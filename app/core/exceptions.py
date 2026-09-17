from typing import Optional, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse

class DomainException(Exception):
    """Base domain exception."""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR", status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code

class EntityNotFoundException(DomainException):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found", entity_type: Optional[str] = None, entity_id: Optional[str] = None):
        super().__init__(message=message, code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)
        self.entity_type = entity_type
        self.entity_id = entity_id

class ValidationException(DomainException):
    """Raised when business validation fails."""
    def __init__(self, message: str):
        super().__init__(message=message, code="VALIDATION_ERROR", status_code=status.HTTP_400_BAD_REQUEST)

class StorageException(DomainException):
    """Raised when data storage operation fails."""
    def __init__(self, message: str = "Failed to process data storage"):
        super().__init__(message=message, code="STORAGE_ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "code": exc.code
        }
    )
