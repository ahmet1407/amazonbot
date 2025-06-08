from scraper_amazon import scrape_amazon
from scraper_hepsiburada import scrape_hepsiburada
from scraper_trendyol import scrape_trendyol

def scrape_link(input_text):
    text = input_text.lower()

    # Linkse kontrol et
    if "amazon" in text:
        return scrape_amazon(input_text)
    elif "hepsiburada" in text:
        return scrape_hepsiburada(input_text)
    elif "trendyol" in text:
        return scrape_trendyol(input_text)

    # İsimse yönlendir
    elif "dyson" in text and "v15" in text:
        return scrape_amazon("Dyson V15 Detect")
    elif "supersonic" in text or "kurutma" in text:
        return scrape_hepsiburada("Dyson Supersonic Nural")
    elif "air fryer" in text or "xiaomi" in text:
        return scrape_trendyol("Xiaomi Mi Air Fryer")

    else:
        raise ValueError("Desteklenmeyen platform.")
