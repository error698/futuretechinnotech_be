from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from app.api.deps import get_product_service
from app.services.product_service import ProductService
from app.schemas.product import ProductListResponse, ProductDetailResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=ProductListResponse)
def get_products(
    category: Optional[str] = Query(default=None, description="Filter by product category"),
    car: Optional[str] = Query(default=None, description="Filter by compatible vehicle model"),
    search: Optional[str] = Query(default=None, description="Fuzzy search across names, categories, descriptions, materials"),
    limit: int = Query(default=50, ge=1, le=200, description="Items per page"),
    page: int = Query(default=1, ge=1, description="Page index"),
    service: ProductService = Depends(get_product_service)
):
    """Retrieve filtered, searched, and paginated automotive accessory catalog."""
    return service.list_products(
        category=category,
        car=car,
        search=search,
        limit=limit,
        page=page
    )

@router.get("/{product_id}", response_model=ProductDetailResponse)
def get_product_by_id(
    product_id: str = Path(..., description="Unique product identifier (e.g. ftit-001)"),
    service: ProductService = Depends(get_product_service)
):
    """Retrieve full specifications for a single product and related category accessories."""
    return service.get_product(product_id=product_id)
