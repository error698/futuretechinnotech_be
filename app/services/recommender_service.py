from typing import Dict, Any, List
from app.repositories.product_repo import ProductRepository
from app.schemas.recommendation import RecommendationResponse

class RecommenderService:
    """AI accessory recommendation service tailored by vehicle and driver priority."""

    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def recommend(self, car_model: str = "Toyota Hycross", priority: str = "all", limit: int = 8) -> RecommendationResponse:
        products = self.product_repo.get_all()
        car_model_lower = car_model.lower().strip()

        # 1. Filter by vehicle compatibility
        matched = []
        for p in products:
            compat = [c.lower() for c in p.get("compatible_cars", [])]
            if any(car_model_lower in c for c in compat) or "universal fit" in compat:
                matched.append(p)

        # 2. Priority scoring
        p_lower = priority.lower().strip()
        if p_lower == "interior":
            matched.sort(key=lambda x: 0 if "interior" in x.get("category", "").lower() or "comfort" in x.get("category", "").lower() else 1)
        elif p_lower == "exterior":
            matched.sort(key=lambda x: 0 if "exterior" in x.get("category", "").lower() or "aerodynamics" in x.get("category", "").lower() else 1)
        elif p_lower == "ev":
            matched.sort(key=lambda x: 0 if "ev" in x.get("category", "").lower() else 1)
        elif p_lower == "care":
            matched.sort(key=lambda x: 0 if "care" in x.get("category", "").lower() else 1)

        recommendations = matched[:limit]

        return RecommendationResponse(
            vehicle=car_model,
            priority=priority,
            total_compatible=len(matched),
            recommendations=recommendations
        )
