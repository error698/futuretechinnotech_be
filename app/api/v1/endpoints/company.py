from fastapi import APIRouter, Depends
from app.api.deps import get_product_service
from app.services.product_service import ProductService
from app.schemas.company import CompanyResponse

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("", response_model=CompanyResponse)
def get_company_info(service: ProductService = Depends(get_product_service)):
    """Retrieve Futuretech Innotech corporate profile, facilities, certifications, and contacts."""
    return service.get_company()
