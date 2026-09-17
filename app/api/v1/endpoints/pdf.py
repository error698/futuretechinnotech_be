from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.api.deps import get_pdf_service
from app.services.pdf_service import PdfService
from app.schemas.inquiry import RFQCreate
from app.core.logging import logger

router = APIRouter(tags=["PDF Engine"])

@router.post("/generate-rfq-pdf")
def generate_rfq_pdf(
    payload: RFQCreate,
    service: PdfService = Depends(get_pdf_service)
):
    """Generate official FTIT branded PDF specification & quotation document."""
    try:
        pdf_bytes = service.generate_rfq_quotation(payload.model_dump())
        filename = f"{payload.rfqNumber or 'FTIT_Quotation'}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compile quotation PDF: {str(e)}"
        )
