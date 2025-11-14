"""
Prometheus metrics for monitoring.
"""

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    Counter = None
    Histogram = None
    Gauge = None
    generate_latest = None
    CONTENT_TYPE_LATEST = None

import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Define metrics only if prometheus is available
if PROMETHEUS_AVAILABLE:
    http_requests_total = Counter(
        "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
    )

    http_request_duration_seconds = Histogram(
        "http_request_duration_seconds", "HTTP request duration in seconds", ["method", "endpoint"]
    )

    http_requests_in_progress = Gauge(
        "http_requests_in_progress", "HTTP requests currently in progress", ["method", "endpoint"]
    )

    database_connections = Gauge("database_connections", "Number of active database connections")

    active_users = Gauge("active_users", "Number of active users")
else:
    http_requests_total = None
    http_request_duration_seconds = None
    http_requests_in_progress = None
    database_connections = None
    active_users = None


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to collect HTTP metrics for Prometheus.
    """

    async def dispatch(self, request: Request, call_next):
        # Skip metrics collection if prometheus is not available
        if not PROMETHEUS_AVAILABLE:
            return await call_next(request)

        # Skip metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)

        method = request.method
        endpoint = request.url.path

        # Track in-progress requests
        http_requests_in_progress.labels(method=method, endpoint=endpoint).inc()

        # Start timer
        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Record metrics
            duration = time.time() - start_time
            http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

            http_requests_total.labels(
                method=method, endpoint=endpoint, status=response.status_code
            ).inc()

            return response

        finally:
            # Decrease in-progress counter
            http_requests_in_progress.labels(method=method, endpoint=endpoint).dec()


def get_metrics():
    """
    Get Prometheus metrics.
    """
    if not PROMETHEUS_AVAILABLE:
        return Response(
            content="Prometheus metrics not available. Install prometheus-client package.",
            status_code=503,
        )
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
