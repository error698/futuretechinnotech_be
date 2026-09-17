from fastapi import APIRouter, Depends, Query
from app.api.deps import get_recommender_service
from app.services.recommender_service import RecommenderService
from app.schemas.recommendation import RecommendationResponse

router = APIRouter(tags=["AI Advisor"])

@router.get("/recommend", response_model=RecommendationResponse)
def get_recommendations(
    car: str = Query(default="Toyota Hycross", description="Vehicle make/model"),
    priority: str = Query(default="all", description="Driving priority: all, interior, exterior, ev, care"),
    limit: int = Query(default=8, ge=1, le=50, description="Max accessories to recommend"),
    service: RecommenderService = Depends(get_recommender_service)
):
    """Recommend accessories tailored for a specific car model and driver priority."""
    return service.recommend(car_model=car, priority=priority, limit=limit)
