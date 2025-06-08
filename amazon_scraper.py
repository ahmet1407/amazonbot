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

    soup = BeautifulSoup(response.text, "html.parser")

    # Ürün adı
    try:
        title = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
    except:
        title = "Ürün adı alınamadı"

    # Fiyat
    try:
        price_whole = soup.find("span", {"class": "a-price-whole"})
        price_fraction = soup.find("span", {"class": "a-price-fraction"})
        price = f"{price_whole.text.strip()},{price_fraction.text.strip()} USD"
    except:
        price = "Fiyat alınamadı USD"

    # Puan ve yorumlar
    try:
        rating = soup.find("span", {"class": "a-icon-alt"}).get_text(strip=True).split(" ")[0]
    except:
        rating = "0"

    try:
        review_count_tag = soup.find("span", {"id": "acrCustomerReviewText"})
        review_count = int(re.sub(r"[^\d]", "", review_count_tag.text)) if review_count_tag else 0
    except:
        review_count = 0

    # Yorumlar metinsel olarak alınamıyor (SPA yapısından dolayı), bu yüzden skorları yapay veriyoruz
    pos_score = int(float(rating) / 5 * review_count)
    neg_score = review_count - pos_score

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count,
        "positive_mentions": pos_score,
        "negative_mentions": neg_score
    }
