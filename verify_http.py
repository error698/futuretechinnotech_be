import requests
import json
import time

BASE = "http://localhost:8000"

def test_http():
    print(f"Testing live HTTP connection to {BASE}...")

    # 1. Health Probe
    r = requests.get(f"{BASE}/health", timeout=5)
    print("GET /health ->", r.status_code, r.json())
    assert r.status_code == 200

    # 2. OpenAPI Documentation
    r = requests.get(f"{BASE}/openapi.json", timeout=5)
    print(f"GET /openapi.json -> {r.status_code}, routes count: {len(r.json().get('paths', {}))}")
    assert r.status_code == 200

    # 3. Versioned Products (/api/v1/products)
    r = requests.get(f"{BASE}/api/v1/products?limit=2&page=1", timeout=5)
    data = r.json()
    print(f"GET /api/v1/products -> {r.status_code}, total: {data.get('total')}, returned: {len(data.get('products', []))}")
    assert r.status_code == 200
    assert len(data.get('products', [])) == 2

    # 4. Legacy Products Alias (/api/products)
    r = requests.get(f"{BASE}/api/products?limit=2&page=1", timeout=5)
    assert r.status_code == 200
    print(f"GET /api/products (Legacy alias) -> {r.status_code} OK")

    # 5. Versioned Categories (/api/v1/categories)
    r = requests.get(f"{BASE}/api/v1/categories", timeout=5)
    data = r.json()
    print(f"GET /api/v1/categories -> {r.status_code}, categories: {len(data.get('categories', []))}")
    assert r.status_code == 200

    # 6. Versioned Company Info (/api/v1/company)
    r = requests.get(f"{BASE}/api/v1/company", timeout=5)
    print(f"GET /api/v1/company -> {r.status_code}, has company: {'company' in r.json()}")
    assert r.status_code == 200

    # 7. Versioned RFQ Submission (/api/v1/rfq)
    payload = {
        "name": "Live HTTP Enterprise Client",
        "email": "enterprise-live@ftit.in",
        "phone": "+91 99999 55555",
        "company": "Live Fleet Corp",
        "vehicle": "Toyota Hycross",
        "items": [{"name": "Roof Rails", "quantity": 1}],
        "message": "Testing v1 RFQ endpoint"
    }
    r = requests.post(f"{BASE}/api/v1/rfq", json=payload, timeout=5)
    print(f"POST /api/v1/rfq -> {r.status_code}, rfqNumber: {r.json().get('rfqNumber')}")
    assert r.status_code == 201

    # 8. Legacy RFQ Alias (/api/rfq)
    r = requests.post(f"{BASE}/api/rfq", json=payload, timeout=5)
    print(f"POST /api/rfq (Legacy alias) -> {r.status_code} OK")
    assert r.status_code == 201

    # 9. Versioned Contact (/api/v1/contact)
    contact_payload = {
        "name": "Live Contact Tester",
        "email": "contact-live@ftit.in",
        "phone": "+91 99999 66666",
        "subject": "Live API Architecture Verification",
        "message": "Testing modular clean architecture router"
    }
    r = requests.post(f"{BASE}/api/v1/contact", json=contact_payload, timeout=5)
    print(f"POST /api/v1/contact -> {r.status_code}, inquiryId: {r.json().get('inquiryId')}")
    assert r.status_code == 201

    # 10. AI Recommender (/api/v1/recommend & /api/py/recommend)
    r = requests.get(f"{BASE}/api/v1/recommend?car=Toyota%20Hycross&limit=3", timeout=5)
    assert r.status_code == 200
    r_legacy = requests.get(f"{BASE}/api/py/recommend?car=Toyota%20Hycross&limit=3", timeout=5)
    assert r_legacy.status_code == 200
    print(f"GET /api/v1/recommend & /api/py/recommend -> Both 200 OK")

    # 11. PDF Generation (/api/v1/generate-rfq-pdf & /api/py/generate-rfq-pdf)
    r = requests.post(f"{BASE}/api/v1/generate-rfq-pdf", json=payload, timeout=5)
    assert r.status_code == 200
    assert "application/pdf" in r.headers.get("content-type", "")
    print(f"POST /api/v1/generate-rfq-pdf -> 200 OK (PDF bytes: {len(r.content)})")

    # 12. Domain Exception Handling (404 for unknown product)
    r = requests.get(f"{BASE}/api/v1/products/non-existent-product-id", timeout=5)
    print(f"GET /api/v1/products/invalid -> {r.status_code} (Code: {r.json().get('code')})")
    assert r.status_code == 404
    assert r.json().get("code") == "NOT_FOUND"

    print("\n==================================================")
    print("  ALL LIVE HTTP & ARCHITECTURE CHECKS PASSED!     ")
    print("==================================================")

if __name__ == "__main__":
    test_http()
