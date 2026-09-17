from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    products,
    categories,
    company,
    inquiries,
    ai,
    pdf,
    sync,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(company.router)
api_router.include_router(inquiries.router)
api_router.include_router(ai.router)
api_router.include_router(pdf.router)
api_router.include_router(sync.router)
