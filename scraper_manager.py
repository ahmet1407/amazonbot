from detect_platform import detect_platform
from scrape_amazon import scrape_amazon
from scrape_hepsiburada import scrape_hepsiburada
from serpapi_search import search_link

def scrape_link(link: str):
    platform = detect_platform(link)

    if platform == "amazon":
        return scrape_amazon(link)
    elif platform == "hepsiburada":
        return scrape_hepsiburada(link)
    else:
        return search_link(link)  # fallback to SerpAPI
