import requests

def search_link(link: str):
    from urllib.parse import quote

    SERPAPI_KEY = "your_serpapi_key"
    q = quote(link)
    serpapi_url = f"https://serpapi.com/search.json?engine=google&q={q}&api_key={SERPAPI_KEY}&device=desktop"

    try:
        response = requests.get(serpapi_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Try to find matching organic result
        best_match = None
        for result in data.get("organic_results", []):
            if result.get("link") and link in result.get("link"):
                best_match = result
                break

        if best_match:
            return {
                "title": best_match.get("title"),
                "link": best_match.get("link"),
                "description": best_match.get("snippet"),
                "rating": best_match.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("rating"),
                "review_count": best_match.get("rich_snippet", {}).get("top", {}).get("detected_extensions", {}).get("reviews"),
            }

        return {"error": "No match found in SERP results."}

    except Exception as e:
        return {"error": str(e)}
