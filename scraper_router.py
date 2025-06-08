from scraper_amazon import scrape_amazon
from scraper_hepsiburada import scrape_hepsiburada
from scraper_trendyol import scrape_trendyol

def scrape_link(url):
    if "amazon.com.tr" in url:
        return scrape_amazon(url)
    elif "hepsiburada.com" in url:
        return scrape_hepsiburada(url)
    elif "trendyol.com" in url:
        return scrape_trendyol(url)
    else:
        raise ValueError("Desteklenmeyen link.")
