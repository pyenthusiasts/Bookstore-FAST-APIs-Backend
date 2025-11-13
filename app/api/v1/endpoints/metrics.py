"""
Metrics endpoint for Prometheus.
"""

from fastapi import APIRouter

from app.core.metrics import get_metrics

router = APIRouter()


@router.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    Returns metrics in Prometheus format.
    """
    return get_metrics()
