import os
import json
import threading
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import StorageException

class InquiryRepository:
    """Thread-safe inquiry repository for RFQs and Contact inquiries."""

    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath or settings.INQUIRIES_FILE
        self._lock = threading.Lock()

    def _read_unsafe(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def get_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._read_unsafe())

    def get_by_id(self, inquiry_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            inquiries = self._read_unsafe()
            return next((i for i in inquiries if i.get("id") == inquiry_id), None)

    def add(self, record: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            try:
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
                inquiries = self._read_unsafe()
                inquiries.insert(0, record)
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump(inquiries, f, indent=2, ensure_ascii=False)
                return record
            except Exception as e:
                logger.error(f"Failed to persist inquiry record: {e}")
                raise StorageException(f"Failed to save inquiry: {str(e)}")
