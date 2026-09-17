from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class RecommendationResponse(BaseModel):
    vehicle: str
    priority: str
    total_compatible: int
    recommendations: List[Dict[str, Any]]

class SyncStatusResponse(BaseModel):
    status: str
    message: str
    statusCode: Optional[int] = None
    connected: bool
