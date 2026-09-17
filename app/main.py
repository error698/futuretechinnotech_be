import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.exceptions import DomainException, domain_exception_handler
from app.core.logging import logger
from app.api.v1.router import api_router

# Individual routers for legacy / backward-compatibility aliases
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

def create_application() -> FastAPI:
    """Application factory for FTIT Backend API."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description=settings.PROJECT_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # 1. Global CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Global Exception Handlers
    app.add_exception_handler(DomainException, domain_exception_handler)

    # 3. Mount Primary Versioned API (/api/v1)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # 4. Mount Legacy / Backward-Compatible Aliases
    # Top-level /health
    app.include_router(health.router)
    # /api/products, /api/categories, /api/company, /api/rfq, /api/contact
    app.include_router(products.router, prefix="/api")
    app.include_router(categories.router, prefix="/api")
    app.include_router(company.router, prefix="/api")
    app.include_router(inquiries.router, prefix="/api")
    # /api/py/recommend, /api/recommend
    app.include_router(ai.router, prefix="/api/py")
    app.include_router(ai.router, prefix="/api")
    # /api/py/generate-rfq-pdf, /api/generate-rfq-pdf
    app.include_router(pdf.router, prefix="/api/py")
    app.include_router(pdf.router, prefix="/api")
    # /api/py/sync, /api/sync
    app.include_router(sync.router, prefix="/api/py")
    app.include_router(sync.router, prefix="/api")

    # 5. Production Static Frontend Serving (SPA)
    if os.path.exists(settings.FRONTEND_DIST):
        assets_dir = os.path.join(settings.FRONTEND_DIST, "assets")
        images_dir = os.path.join(settings.FRONTEND_DIST, "images")

        if os.path.exists(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        if os.path.exists(images_dir):
            app.mount("/images", StaticFiles(directory=images_dir), name="images")

        @app.get("/{full_path:path}")
        async def serve_spa(request: Request, full_path: str):
            # Do not intercept API, docs, or OpenAPI endpoints
            if full_path.startswith("api") or full_path in ("health", "docs", "redoc", "openapi.json"):
                raise HTTPException(status_code=404, detail="Not Found")
            file_path = os.path.join(settings.FRONTEND_DIST, full_path)
            if os.path.isfile(file_path):
                return FileResponse(file_path)
            return FileResponse(os.path.join(settings.FRONTEND_DIST, "index.html"))

    logger.info("FTIT FastAPI Application successfully initialized.")
    return app

app = create_application()
