# utils/scrape_hepsiburada.py

import requests
import json
import re

def scrape_hepsiburada(serpapi_key, product_url):
    search_url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": product_url,
        "api_key": serpapi_key,
        "device": "desktop",
        "google_domain": "google.com"
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    try:
        results = data.get("organic_results", [])
        for result in results:
            if "link" in result and product_url in result["link"]:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                rating = result.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("rating", None)
                reviews = result.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("reviews", None)

                return {
                    "name": title,
                    "description": snippet,
                    "rating": float(rating) * 20 if rating else None,
                    "reviews": reviews
                }
    except Exception as e:
        print(f"Error parsing Hepsiburada result: {e}")

    return {
        "name": None,
        "description": None,
        "rating": None,
        "reviews": None
    }
