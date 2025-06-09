from scraper_amazon import scrape_amazon
from scraper_hepsiburada import scrape_hepsiburada
from scraper_trendyol import scrape_trendyol

def scrape_link(input_text):
    text = input_text.lower()

    if "amazon" in text:
        return scrape_amazon(input_text)
    elif "hepsiburada" in text:
        return scrape_hepsiburada(input_text)
    elif "trendyol" in text:
        return scrape_trendyol(input_text)
    else:
        raise ValueError("Sadece Amazon, Hepsiburada veya Trendyol linkleri destekleniyor.")
