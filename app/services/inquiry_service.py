import time
from datetime import datetime, timezone
from typing import Dict, Any
from app.repositories.inquiry_repo import InquiryRepository
from app.schemas.inquiry import RFQCreate, RFQResponse, ContactCreate, ContactResponse
from app.core.exceptions import ValidationException

class InquiryService:
    """Business logic service for quotations (RFQ) and contact messages."""

    def __init__(self, inquiry_repo: InquiryRepository):
        self.inquiry_repo = inquiry_repo

    def process_rfq(self, payload: RFQCreate) -> RFQResponse:
        if not payload.name.strip():
            raise ValidationException("Name is required.")
        if not payload.email.strip():
            raise ValidationException("Email address is required.")
        if not payload.items:
            raise ValidationException("Please provide at least one quotation item.")

        timestamp_ms = int(time.time() * 1000)
        rfq_id = payload.rfqNumber or f"RFQ-{timestamp_ms}"

        rfq_record = {
            "id": rfq_id,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "type": "RFQ_QUOTE_REQUEST",
            "name": payload.name.strip(),
            "email": payload.email.strip(),
            "phone": payload.phone.strip() if payload.phone else "Not provided",
            "company": payload.company.strip() if payload.company else "Individual / Aftermarket",
            "vehicle": payload.vehicle.strip() if payload.vehicle else "Universal",
            "itemCount": len(payload.items),
            "items": payload.items,
            "message": payload.message.strip() if payload.message else "",
            "status": "PENDING_ENGINEERING_REVIEW"
        }

        saved = self.inquiry_repo.add(rfq_record)

        return RFQResponse(
            success=True,
            message="Your Request for Quotation has been received by Futuretech Innotech engineering team.",
            rfqNumber=saved["id"],
            data=saved
        )

    def process_contact(self, payload: ContactCreate) -> ContactResponse:
        if not payload.name.strip():
            raise ValidationException("Name is required.")
        if not payload.email.strip():
            raise ValidationException("Email address is required.")
        if not payload.message.strip():
            raise ValidationException("Message cannot be empty.")

        timestamp_ms = int(time.time() * 1000)
        msg_id = f"MSG-{timestamp_ms}"

        contact_record = {
            "id": msg_id,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "type": "GENERAL_CONTACT",
            "name": payload.name.strip(),
            "email": payload.email.strip(),
            "phone": payload.phone.strip() if payload.phone else "",
            "subject": payload.subject.strip() if payload.subject else "General Inquiry",
            "message": payload.message.strip(),
            "status": "RECEIVED"
        }

        saved = self.inquiry_repo.add(contact_record)

        return ContactResponse(
            success=True,
            message="Thank you for reaching out! Our team in New Delhi will contact you shortly.",
            inquiryId=saved["id"]
        )
