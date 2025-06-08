from scraper_amazon import scrape_amazon
from scraper_hepsiburada import scrape_hepsiburada
from scraper_trendyol import scrape_trendyol

def scrape_link(url):
    if "amazon" in url:
        return scrape_amazon(url)
    elif "hepsiburada" in url:
        return scrape_hepsiburada(url)
    elif "trendyol" in url:
        return scrape_trendyol(url)
    else:
        raise Exception("Desteklenmeyen platform.")
