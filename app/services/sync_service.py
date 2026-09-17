import requests
from app.core.config import settings
from app.core.logging import logger
from app.schemas.recommendation import SyncStatusResponse

class SyncService:
    """Catalog crawler and external synchronization service."""

    def __init__(self, base_url: str = settings.SCRAPER_BASE_URL):
        self.base_url = base_url

    def check_connection(self) -> SyncStatusResponse:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FTIT-SyncEngine/2.1"}
        target_url = f"{self.base_url}/our-products-01/"
        try:
            r = requests.get(target_url, headers=headers, timeout=10)
            is_connected = (r.status_code == 200)
            return SyncStatusResponse(
                status="success" if is_connected else "warning",
                message=f"Live sync probe returned status {r.status_code}",
                statusCode=r.status_code,
                connected=is_connected
            )
        except Exception as e:
            logger.warning(f"Sync check failed: {e}")
            return SyncStatusResponse(
                status="error",
                message=str(e),
                statusCode=None,
                connected=False
            )
