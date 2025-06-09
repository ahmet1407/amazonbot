import os
import requests

def scrape_amazon(url):
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        raise ValueError("SerpAPI API key bulunamadı.")

    params = {
        "api_key": api_key,
        "engine": "amazon_product",
        "url": url
    }

    response = requests.get("https://serpapi.com/search.json", params=params)
    data = response.json()

    # Debug log
    print("📦 SerpAPI Amazon verisi:", data)

    if "error" in data:
        raise ValueError(f"SerpAPI Hatası: {data['error']}")

    return {
        "name": data.get("title", "Ürün adı bulunamadı"),
        "price": data.get("price", "Fiyat bulunamadı"),
        "segment": "Orta",
        "reviews": [r.get("snippet", "") for r in data.get("reviews", [])][:3],
        "expert_score": 87
    }
