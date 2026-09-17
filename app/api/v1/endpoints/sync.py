from fastapi import APIRouter, Depends
from app.api.deps import get_sync_service
from app.services.sync_service import SyncService
from app.schemas.recommendation import SyncStatusResponse

router = APIRouter(tags=["Catalog Sync"])

@router.get("/sync", response_model=SyncStatusResponse)
def trigger_sync_probe(service: SyncService = Depends(get_sync_service)):
    """Check connectivity and trigger sync check with futuretechinnotech.in."""
    return service.check_connection()
