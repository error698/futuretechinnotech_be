from fastapi import APIRouter, Depends
from app.api.deps import get_product_service
from app.services.product_service import ProductService
from app.schemas.product import CategoriesResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=CategoriesResponse)
def get_categories(service: ProductService = Depends(get_product_service)):
    """Retrieve distinct catalog categories and inventory statistics."""
    return service.get_categories()
