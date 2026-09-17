import os
import json
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.repositories.base import BaseRepository

class ProductRepository(BaseRepository[Dict[str, Any]]):
    """File-backed product repository with in-memory caching."""

    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath or settings.PRODUCTS_FILE
        self._cache: Optional[List[Dict[str, Any]]] = None
        self._last_mtime: float = 0.0

    def _load_data(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.filepath):
            logger.warning(f"Products file not found at {self.filepath}")
            return []

        try:
            mtime = os.path.getmtime(self.filepath)
            if self._cache is not None and mtime == self._last_mtime:
                return self._cache

            with open(self.filepath, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
                self._last_mtime = mtime
                return self._cache
        except Exception as e:
            logger.error(f"Error loading products from {self.filepath}: {e}")
            return self._cache or []

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self._load_data())

    def get_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        pid = product_id.strip().lower()
        for product in self._load_data():
            if product.get("id", "").strip().lower() == pid:
                return product
        return None

    def get_categories(self) -> List[str]:
        seen = set()
        categories = []
        for p in self._load_data():
            cat = p.get("category", "General")
            if cat not in seen:
                seen.add(cat)
                categories.append(cat)
        return categories

    def get_stats_by_category(self) -> List[Dict[str, Any]]:
        products = self._load_data()
        categories = self.get_categories()
        return [
            {"name": cat, "count": sum(1 for p in products if p.get("category") == cat)}
            for cat in categories
        ]
