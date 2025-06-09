import os
import requests
import re

def extract_product_id(url):
    match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", url)
    if match:
        return match.group(1)
    return None

def scrape_amazon(url):
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SERPAPI_KEY bulunamadı")

    product_id = extract_product_id(url)
    if not product_id:
        raise ValueError("Amazon ürün ID'si çıkarılamadı.")

    params = {
        "engine": "amazon",
        "q": product_id,
        "amazon_domain": "amazon.com.tr",
        "api_key": api_key
    }

    response = requests.get("https://serpapi.com/search.json", params=params)
    data = response.json()

    # İlk ürün sonucunu al
    product = data.get("shopping_results", [{}])[0]
    reviews = [r["snippet"] for r in data.get("reviews", [])[:3]]

    return {
        "name": product.get("title", "Ürün adı bulunamadı"),
        "price": product.get("price", "Fiyat bulunamadı"),
        "segment": "Orta",
        "reviews": reviews,
        "expert_score": 87
    }
