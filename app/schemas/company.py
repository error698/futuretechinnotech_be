from typing import Optional, Any, Dict
from pydantic import BaseModel

class CompanyResponse(BaseModel):
    success: bool = True
    company: Optional[Dict[str, Any]] = None
    stats: Optional[Dict[str, Any]] = None
    certifications: Optional[Any] = None
    model_config = {"extra": "allow"}
