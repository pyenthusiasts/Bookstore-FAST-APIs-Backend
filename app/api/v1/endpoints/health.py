"""
Health check endpoints for monitoring and orchestration.
"""
import time
from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

# Application start time
START_TIME = time.time()


@router.get("/health", status_code=status.HTTP_200_OK)
def basic_health_check():
    """
    Basic health check endpoint.
    Returns 200 if the application is running.
    """
    return {"status": "healthy"}


@router.get("/health/ready", status_code=status.HTTP_200_OK)
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check - verifies the application is ready to serve traffic.
    Checks database connectivity.
    """
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        db_status = "connected"
        db_healthy = True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = f"error: {str(e)}"
        db_healthy = False

    if not db_healthy:
        return {
            "status": "unhealthy",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat(),
        }

    return {
        "status": "ready",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/live", status_code=status.HTTP_200_OK)
def liveness_check():
    """
    Liveness check - verifies the application is alive.
    Used by orchestrators to determine if the app needs to be restarted.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check with comprehensive system information.
    """
    uptime = time.time() - START_TIME

    # Check database
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
        db_latency_start = time.time()
        db.execute(text("SELECT 1"))
        db_latency = (time.time() - db_latency_start) * 1000  # ms
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"
        db_latency = None

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "version": settings.APP_VERSION,
        "uptime_seconds": round(uptime, 2),
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": {
                "status": db_status,
                "latency_ms": round(db_latency, 2) if db_latency else None,
            },
        },
    }
