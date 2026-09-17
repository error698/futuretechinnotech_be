import sys
import os

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.repositories.product_repo import ProductRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.inquiry_repo import InquiryRepository
from app.services.product_service import ProductService
from app.services.inquiry_service import InquiryService
from app.services.recommender_service import RecommenderService
from app.services.pdf_service import PdfService
from app.schemas.inquiry import RFQCreate, ContactCreate

def run_tests():
    print("=== STARTING FTIT ENTERPRISE ARCHITECTURE TESTS ===")
    
    # 1. Repositories
    product_repo = ProductRepository()
    all_prods = product_repo.get_all()
    assert len(all_prods) > 0, "Product repo returned empty"
    first_id = all_prods[0]["id"]
    print(f"[PASS] ProductRepository: Loaded {len(all_prods)} products")

    single_prod = product_repo.get_by_id(first_id)
    assert single_prod is not None
    assert single_prod["id"] == first_id
    print(f"[PASS] ProductRepository: get_by_id('{first_id}') verified")

    company_repo = CompanyRepository()
    company_data = company_repo.get_company_data()
    assert "company" in company_data
    print("[PASS] CompanyRepository: Loaded company data")

    inquiry_repo = InquiryRepository()
    inquiries_list = inquiry_repo.get_all()
    print(f"[PASS] InquiryRepository: Thread-safe storage loaded ({len(inquiries_list)} inquiries)")

    # 2. Product Service
    product_service = ProductService(product_repo, company_repo)
    p_list = product_service.list_products(limit=10, page=1)
    assert p_list.success is True
    assert len(p_list.products) == 10
    print(f"[PASS] ProductService: list_products (Total: {p_list.total}, Page items: {len(p_list.products)})")

    # Search filter
    search_res = product_service.list_products(search="Coffee", limit=5)
    assert search_res.success is True
    assert len(search_res.products) > 0
    print(f"[PASS] ProductService: Search filter found {len(search_res.products)} items")

    # Vehicle filter
    car_res = product_service.list_products(car="Toyota Hycross", limit=5)
    assert car_res.success is True
    assert len(car_res.products) > 0
    print(f"[PASS] ProductService: Vehicle compatibility found {len(car_res.products)} items")

    # Product detail
    detail = product_service.get_product(first_id)
    assert detail.success is True
    assert detail.product.id == first_id
    assert len(detail.related) > 0
    print(f"[PASS] ProductService: get_product ('{first_id}', {len(detail.related)} related)")

    # Categories
    cats = product_service.get_categories()
    assert cats.success is True
    assert len(cats.categories) > 0
    print(f"[PASS] ProductService: get_categories ({len(cats.categories)} categories)")

    # 3. Inquiry Service
    inquiry_service = InquiryService(inquiry_repo)
    rfq_payload = RFQCreate(
        name="Enterprise Client Test",
        email="enterprise@ftit.in",
        phone="+91 98765 11111",
        company="Fleet Solutions Corp",
        vehicle="Toyota Hycross",
        items=[{"id": first_id, "name": "Coffee Maker", "quantity": 1}],
        message="Requesting enterprise fleet quotation."
    )
    rfq_res = inquiry_service.process_rfq(rfq_payload)
    assert rfq_res.success is True
    assert rfq_res.rfqNumber.startswith("RFQ-")
    print(f"[PASS] InquiryService: process_rfq generated {rfq_res.rfqNumber}")

    contact_payload = ContactCreate(
        name="Enterprise Contact Test",
        email="contact@ftit.in",
        phone="+91 98765 22222",
        subject="OEM Tier-1 Supply Agreement",
        message="Discussion for new model accessory package supply."
    )
    contact_res = inquiry_service.process_contact(contact_payload)
    assert contact_res.success is True
    assert contact_res.inquiryId.startswith("MSG-")
    print(f"[PASS] InquiryService: process_contact generated {contact_res.inquiryId}")

    # 4. Recommender Service
    rec_service = RecommenderService(product_repo)
    recs = rec_service.recommend(car_model="Toyota Hycross", priority="all", limit=4)
    assert len(recs.recommendations) > 0
    print(f"[PASS] RecommenderService: Generated {len(recs.recommendations)} accessory recommendations")

    # 5. PDF Service
    pdf_service = PdfService()
    pdf_bytes = pdf_service.generate_rfq_quotation(rfq_payload.model_dump())
    assert len(pdf_bytes) > 1000
    print(f"[PASS] PdfService: Compiled official quotation PDF ({len(pdf_bytes)} bytes)")

    print("\n==================================================")
    print("  ALL ARCHITECTURE & SERVICE TESTS PASSED!        ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
