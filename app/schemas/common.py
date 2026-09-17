from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class BaseResponse(BaseModel):
    success: bool = True
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    code: Optional[str] = None

class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str
    version: str
    framework: str
    timestamp: str
