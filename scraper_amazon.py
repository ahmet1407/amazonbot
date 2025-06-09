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
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    return {
        "name": data.get("title", "Ürün adı bulunamadı"),
        "price": data.get("price", "Fiyat bulunamadı"),
        "segment": "Orta",
        "reviews": [r.get("snippet", "") for r in data.get("reviews", [])][:3],
        "expert_score": 87
    }
