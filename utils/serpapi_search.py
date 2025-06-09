import requests
import os

SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")

def get_best_link_from_search(query: str) -> str:
    params = {
        "engine": "google",
        "q": query,
        "num": 10,
        "api_key": SERPAPI_API_KEY
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    results = data.get("organic_results", [])

    for result in results:
        link = result.get("link")
        if "amazon.com.tr" in link or "hepsiburada.com" in link:
            return link  # Öncelikli platformlar
    return results[0].get("link") if results else None
