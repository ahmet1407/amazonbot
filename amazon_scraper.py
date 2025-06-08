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
        return {"error": f"Bağlantı sağlanamadı: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        title = soup.find(id="productTitle").get_text(strip=True)
    except:
        title = "Ürün başlığı alınamadı"

    try:
        price_tag = soup.find("span", {"class": re.compile(".*price.*")})
        if not price_tag:
            price_tag = soup.find("span", {"class": "a-offscreen"})
        price = price_tag.get_text(strip=True)
    except:
        price = "Fiyat alınamadı"

    try:
        rating_tag = soup.find("span", {"class": "a-icon-alt"})
        rating = rating_tag.get_text(strip=True).split(" ")[0]
    except:
        rating = "Puan alınamadı"

    try:
        review_tag = soup.find("span", {"id": "acrCustomerReviewText"})
        review_count = review_tag.get_text(strip=True).split(" ")[0]
    except:
        review_count = "Yorum sayısı alınamadı"

    return {
        "name": title,
        "price": price,
        "rating": rating,
        "review_count": review_count
    }
