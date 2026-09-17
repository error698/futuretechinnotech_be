from fastapi import APIRouter, Depends, status
from app.api.deps import get_inquiry_service
from app.services.inquiry_service import InquiryService
from app.schemas.inquiry import RFQCreate, RFQResponse, ContactCreate, ContactResponse

router = APIRouter(tags=["Inquiries & Quotations"])

@router.post("/rfq", response_model=RFQResponse, status_code=status.HTTP_201_CREATED)
def submit_rfq(
    payload: RFQCreate,
    service: InquiryService = Depends(get_inquiry_service)
):
    """Submit a Request for Quotation (RFQ) basket for engineering review."""
    return service.process_rfq(payload)

@router.post("/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def submit_contact_inquiry(
    payload: ContactCreate,
    service: InquiryService = Depends(get_inquiry_service)
):
    """Submit general dealership or technical inquiry."""
    return service.process_contact(payload)
