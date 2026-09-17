import math
from typing import Optional, List, Dict, Any
from app.repositories.product_repo import ProductRepository
from app.repositories.company_repo import CompanyRepository
from app.schemas.product import ProductItem, ProductListResponse, ProductDetailResponse, CategoriesResponse, CategoryStat
from app.core.exceptions import EntityNotFoundException

class ProductService:
    """Business logic service for catalog queries, filters, and product details."""

    def __init__(self, product_repo: ProductRepository, company_repo: CompanyRepository):
        self.product_repo = product_repo
        self.company_repo = company_repo

    def list_products(
        self,
        category: Optional[str] = None,
        car: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        page: int = 1
    ) -> ProductListResponse:
        raw_products = self.product_repo.get_all()
        results = list(raw_products)

        # 1. Category filter
        if category and category.strip() and category.strip().lower() != "all":
            cat_lower = category.strip().lower()
            results = [p for p in results if p.get("category", "").strip().lower() == cat_lower]

        # 2. Vehicle compatibility filter
        if car and car.strip() and car.strip().lower() != "all":
            car_lower = car.strip().lower()
            def car_match(p):
                compat = [c.strip().lower() for c in p.get("compatible_cars", [])]
                return any(car_lower in c for c in compat) or "universal fit" in compat
            results = [p for p in results if car_match(p)]

        # 3. Multi-field search
        if search and search.strip():
            q = search.strip().lower()
            def search_match(p):
                name = p.get("name", "").lower()
                cat = p.get("category", "").lower()
                desc = p.get("description", "").lower()
                mat = p.get("material", "").lower()
                compat = [c.lower() for c in p.get("compatible_cars", [])]
                return q in name or q in cat or q in desc or q in mat or any(q in c for c in compat)
            results = [p for p in results if search_match(p)]

        total = len(results)
        start_index = (page - 1) * limit
        paginated_raw = results[start_index:start_index + limit]
        total_pages = math.ceil(total / limit) if limit > 0 else 1

        products = [ProductItem(**item) for item in paginated_raw]

        return ProductListResponse(
            success=True,
            total=total,
            page=page,
            limit=limit,
            totalPages=total_pages,
            products=products
        )

    def get_product(self, product_id: str) -> ProductDetailResponse:
        product_raw = self.product_repo.get_by_id(product_id)
        if not product_raw:
            raise EntityNotFoundException(message=f"Product with ID '{product_id}' was not found.")

        all_products = self.product_repo.get_all()
        related_raw = [
            p for p in all_products
            if p.get("category") == product_raw.get("category") and p.get("id") != product_raw.get("id")
        ][:4]

        return ProductDetailResponse(
            success=True,
            product=ProductItem(**product_raw),
            related=[ProductItem(**item) for item in related_raw]
        )

    def get_categories(self) -> CategoriesResponse:
        categories = self.product_repo.get_categories()
        stats = self.product_repo.get_stats_by_category()
        return CategoriesResponse(
            success=True,
            categories=categories,
            statsByCategory=[CategoryStat(**s) for s in stats]
        )

    def get_company(self) -> Dict[str, Any]:
        data = self.company_repo.get_company_data()
        return {
            "success": True,
            **data
        }
