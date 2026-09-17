from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class ProductItem(BaseModel):
    id: str
    name: str
    category: str
    image: str
    remote_image: Optional[str] = None
    source_page: Optional[str] = None
    compatible_cars: List[str] = Field(default_factory=list)
    material: Optional[str] = None
    finishes: List[str] = Field(default_factory=list)
    warranty: Optional[str] = None
    oem_tier: Optional[str] = None
    description: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    in_stock: Optional[bool] = True
    rfq_available: Optional[bool] = True
    model_config = {"extra": "allow"}

class ProductListResponse(BaseModel):
    success: bool = True
    total: int
    page: int
    limit: int
    totalPages: int
    products: List[ProductItem]

class ProductDetailResponse(BaseModel):
    success: bool = True
    product: ProductItem
    related: List[ProductItem] = Field(default_factory=list)

class CategoryStat(BaseModel):
    name: str
    count: int

class CategoriesResponse(BaseModel):
    success: bool = True
    categories: List[str]
    statsByCategory: List[CategoryStat]
