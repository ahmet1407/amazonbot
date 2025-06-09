import os
import requests
from urllib.parse import urlencode

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def perform_serpapi_search(url: str) -> dict:
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_KEY environment variable not set.")

    params = {
        "engine": "google",
        "q": url,
        "api_key": SERPAPI_KEY,
        "device": "desktop",
        "num": "10"
    }

    endpoint = f"https://serpapi.com/search.json?{urlencode(params)}"
    response = requests.get(endpoint)
    
    if response.status_code != 200:
        raise Exception(f"SerpAPI error: {response.status_code}, {response.text}")

    return response.json()
