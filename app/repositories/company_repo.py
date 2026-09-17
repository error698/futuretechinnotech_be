import os
import json
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger

class CompanyRepository:
    """Repository for corporate and OEM details."""

    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath or settings.COMPANY_FILE

    def get_company_data(self) -> Dict[str, Any]:
        if not os.path.exists(self.filepath):
            logger.warning(f"Company file not found at {self.filepath}")
            return {}

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading company data: {e}")
            return {}
