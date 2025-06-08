import requests
from bs4 import BeautifulSoup
import re

def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Bağlantı hatası: {e}"}

    soup = BeautifulSoup(response.content, "html.parser")

    try:
        title = soup.find(id="productTitle").get_text(strip=True)
    except:
        title = "Ürün adı alınamadı"

    try:
        price_block = soup.find("span", {"class": re.compile(".*price.*")})
        price = price_block.get_text(strip=True) if price_block else "Fiyat alınamadı"
    except:
        price = "Fiyat alınamadı"

    try:
        rating_block = soup.find("span", {"class": re.compile(".*a-icon-alt.*")})
        rating = rating_block.get_text(strip=True).split(" ")[0] if rating_block else "Puan alınamadı"
    except:
        rating = "Puan alınamadı"

    try:
        reviews = soup.find(id="acrCustomerReviewText")
        review_count = reviews.get_text(strip=True).split(" ")[0] if reviews else "0"
    except:
        review_count = "0"

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count
    }
