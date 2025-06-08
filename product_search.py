import requests
import os

def search_product_url(query):
    api_key = os.getenv("SERPAPI_KEY")
    params = {
        "q": query,
        "engine": "google",
        "api_key": api_key,
        "num": 10
    }
    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    for result in results.get("organic_results", []):
        link = result.get("link")
        if any(x in link for x in ["amazon.com", "hepsiburada.com", "trendyol.com"]):
            return link
    return None
