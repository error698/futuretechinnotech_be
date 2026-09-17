from functools import lru_cache
from app.repositories.product_repo import ProductRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.inquiry_repo import InquiryRepository
from app.services.product_service import ProductService
from app.services.inquiry_service import InquiryService
from app.services.recommender_service import RecommenderService
from app.services.pdf_service import PdfService
from app.services.sync_service import SyncService

@lru_cache()
def get_product_repository() -> ProductRepository:
    return ProductRepository()

@lru_cache()
def get_company_repository() -> CompanyRepository:
    return CompanyRepository()

@lru_cache()
def get_inquiry_repository() -> InquiryRepository:
    return InquiryRepository()

def get_product_service() -> ProductService:
    return ProductService(
        product_repo=get_product_repository(),
        company_repo=get_company_repository()
    )

def get_inquiry_service() -> InquiryService:
    return InquiryService(inquiry_repo=get_inquiry_repository())

def get_recommender_service() -> RecommenderService:
    return RecommenderService(product_repo=get_product_repository())

def get_pdf_service() -> PdfService:
    return PdfService()

def get_sync_service() -> SyncService:
    return SyncService()
