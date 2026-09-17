import os
from dataclasses import dataclass, field
from typing import List

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

@dataclass
class Settings:
    PROJECT_NAME: str = "Futuretech Innotech (FTIT) API"
    PROJECT_VERSION: str = "2.1.0"
    PROJECT_DESCRIPTION: str = "Enterprise-grade Tier-1 Automotive REST API & Engineering Engine."
    
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = field(default_factory=lambda: ["*"])
    
    # Data Storage Paths
    DATA_DIR: str = field(default_factory=lambda: os.path.join(BASE_DIR, "data"))
    PRODUCTS_FILE: str = field(default_factory=lambda: os.path.join(BASE_DIR, "data/products.json"))
    COMPANY_FILE: str = field(default_factory=lambda: os.path.join(BASE_DIR, "data/company.json"))
    INQUIRIES_FILE: str = field(default_factory=lambda: os.path.join(BASE_DIR, "data/inquiries.json"))
    
    # Frontend Distribution Directory (for production SPA serving)
    FRONTEND_DIST: str = field(default_factory=lambda: os.path.abspath(os.path.join(BASE_DIR, "../frontend/dist")))
    
    # External Scraper
    SCRAPER_BASE_URL: str = "https://futuretechinnotech.in"

settings = Settings()
