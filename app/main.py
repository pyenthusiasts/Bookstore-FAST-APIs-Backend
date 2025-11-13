"""
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.v1 import api_router
from app.api.v1.endpoints import health
from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging
from app.core.middleware import (
    LoggingMiddleware,
    RateLimitMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)
from app.db.database import engine
from app.models import Base

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    yield
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern, production-ready bookstore API built with FastAPI",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add middleware (order matters - first added is outermost)
# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# Request ID tracking
app.add_middleware(RequestIDMiddleware)

# Logging
app.add_middleware(LoggingMiddleware)

# Rate limiting
if not settings.DEBUG:
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)

# GZIP compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted host (uncomment and configure in production)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com", "*.yourdomain.com"])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

# Metrics endpoint (optional - requires prometheus-client)
try:
    from app.api.v1.endpoints import metrics

    app.include_router(metrics.router, tags=["Monitoring"])
except ImportError:
    logger.warning("Metrics endpoint not available (prometheus-client not installed)")


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint.

    Returns:
        Welcome message
    """
    return {
        "message": "Welcome to the Bookstore API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy"}
