from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def check_health():
    """System liveness and operational readiness check."""
    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        framework="FastAPI",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
