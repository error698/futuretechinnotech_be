from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = "Accessories"
    quantity: Optional[int] = 1
    model_config = {"extra": "allow"}

class RFQCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = "Not provided"
    company: Optional[str] = "Individual / Aftermarket"
    vehicle: Optional[str] = "Universal"
    items: List[Any] = Field(default_factory=list)
    message: Optional[str] = ""
    rfqNumber: Optional[str] = None
    model_config = {"extra": "allow"}

class RFQRecord(BaseModel):
    id: str
    createdAt: str
    type: str = "RFQ_QUOTE_REQUEST"
    name: str
    email: str
    phone: str
    company: str
    vehicle: str
    itemCount: int
    items: List[Any]
    message: str
    status: str = "PENDING_ENGINEERING_REVIEW"
    model_config = {"extra": "allow"}

class RFQResponse(BaseModel):
    success: bool = True
    message: str
    rfqNumber: str
    data: Dict[str, Any]

class ContactCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    subject: Optional[str] = "General Inquiry"
    message: str
    model_config = {"extra": "allow"}

class ContactRecord(BaseModel):
    id: str
    createdAt: str
    type: str = "GENERAL_CONTACT"
    name: str
    email: str
    phone: str
    subject: str
    message: str
    status: str = "RECEIVED"
    model_config = {"extra": "allow"}

class ContactResponse(BaseModel):
    success: bool = True
    message: str
    inquiryId: str
