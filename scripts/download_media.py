import os
import sys
import json
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
PRODUCTS_JSON_BACKEND = os.path.join(BASE_DIR, "backend/data/products.json")
PRODUCTS_JSON_FRONTEND = os.path.join(BASE_DIR, "frontend/src/data/products.json")

PRODUCTS_DIR = os.path.join(BASE_DIR, "frontend/public/images/products")
SITE_DIR = os.path.join(BASE_DIR, "frontend/public/images/site")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SITE_ASSETS = [
    ("ftit-logo-vertical.png", "https://futuretechinnotech.in/wp-content/uploads/2025/09/cropped-cropped-FTIT-Logo-Vertical.png"),
    ("ftit-logotype.png", "https://futuretechinnotech.in/wp-content/uploads/2019/09/logotype.png"),
    ("about-us-hero.png", "https://futuretechinnotech.in/wp-content/uploads/2025/09/About-Us-Image-V2.png"),
]

def download_file(url: str, dest_path: str, retries: int = 3) -> bool:
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 500:
        return True
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200 and len(resp.content) > 0:
                with open(dest_path, "wb") as f:
                    f.write(resp.content)
                return True
            else:
                print(f"[WARN] Status {resp.status_code} for {url}")
        except Exception as e:
            if attempt == retries - 1:
                print(f"[FAIL] Error downloading {url}: {e}")
    return False

def main():
    print("=== FUTURETECH INNOTECH MEDIA DOWNLOADER ===")
    os.makedirs(PRODUCTS_DIR, exist_ok=True)
    os.makedirs(SITE_DIR, exist_ok=True)

    # 1. Download Site Assets
    print("\n1. Downloading Site Branding Assets...")
    for filename, url in SITE_ASSETS:
        dest = os.path.join(SITE_DIR, filename)
        success = download_file(url, dest)
        status = "[DONE]" if success else "[FAILED]"
        print(f"   {status} {filename} ({url})")

    # 2. Download Product Images
    print("\n2. Loading Products Catalog...")
    if not os.path.exists(PRODUCTS_JSON_BACKEND):
        print(f"[ERROR] Cannot find {PRODUCTS_JSON_BACKEND}")
        sys.exit(1)

    with open(PRODUCTS_JSON_BACKEND, "r", encoding="utf-8") as f:
        products = json.load(f)

    print(f"   Found {len(products)} products to process.")

    download_tasks = []
    # Deduplicate image URLs to avoid downloading identical images twice
    url_to_local_name = {}

    for p in products:
        remote_url = p.get("image")
        if not remote_url or not remote_url.startswith("http"):
            continue

        # Preserve remote_image
        if "remote_image" not in p:
            p["remote_image"] = remote_url

        parsed = urllib.parse.urlparse(remote_url)
        raw_name = os.path.basename(parsed.path)
        if not raw_name:
            raw_name = f"{p.get('id', 'product')}.png"

        # Unique destination name
        local_filename = raw_name
        dest_path = os.path.join(PRODUCTS_DIR, local_filename)

        if remote_url not in url_to_local_name:
            url_to_local_name[remote_url] = local_filename
            download_tasks.append((remote_url, dest_path, p.get("id")))

        # Point product image to local public path
        p["image"] = f"/images/products/{local_filename}"

    print(f"\n3. Downloading {len(download_tasks)} unique product images with 8 threads...")

    completed = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_task = {
            executor.submit(download_file, url, dest): (url, dest, pid)
            for url, dest, pid in download_tasks
        }
        for future in as_completed(future_to_task):
            url, dest, pid = future_to_task[future]
            try:
                if future.result():
                    completed += 1
                else:
                    failed += 1
            except Exception as exc:
                print(f"[FAIL] {pid} generated exception: {exc}")
                failed += 1

            if (completed + failed) % 15 == 0 or (completed + failed) == len(download_tasks):
                print(f"   Progress: {completed + failed}/{len(download_tasks)} downloaded ({completed} success, {failed} failed)...")

    print(f"\nCompleted product downloads: {completed} success, {failed} failed.")

    # 4. Save updated products.json in both backend and frontend
    print("\n4. Updating products.json in backend and frontend...")
    with open(PRODUCTS_JSON_BACKEND, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"   [DONE] Updated {PRODUCTS_JSON_BACKEND}")

    if os.path.exists(os.path.dirname(PRODUCTS_JSON_FRONTEND)):
        with open(PRODUCTS_JSON_FRONTEND, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"   [DONE] Updated {PRODUCTS_JSON_FRONTEND}")

    print("\n==================================================")
    print("  ALL MEDIA DOWNLOADED AND CATALOGS UPDATED!      ")
    print("==================================================")

if __name__ == "__main__":
    main()
