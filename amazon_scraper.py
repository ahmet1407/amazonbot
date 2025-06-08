import requests
from bs4 import BeautifulSoup
import re

def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        return {"name": "Erişim hatası", "price": "-", "average_rating": 0, "review_count": 0, "positive_count": 0, "negative_count": 0}

    try:
        name = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
    except:
        name = "Ürün adı alınamadı"

    try:
        price = soup.find("span", {"class": "a-price-whole"}).get_text(strip=True)
    except:
        price = "Fiyat alınamadı"

    try:
        rating = soup.find("span", {"class": "a-icon-alt"}).get_text(strip=True)
        average_rating = float(rating.split(" ")[0])
    except:
        average_rating = 0

    try:
        review_count = soup.find("span", {"id": "acrCustomerReviewText"}).get_text(strip=True)
        review_count = int(review_count.split()[0].replace(",", ""))
    except:
        review_count = 0

    return {
        "name": name,
        "price": price + " USD",
        "average_rating": average_rating,
        "review_count": review_count,
        "positive_count": int(review_count * average_rating / 5),
        "negative_count": int(review_count * (5 - average_rating) / 5)
    }
