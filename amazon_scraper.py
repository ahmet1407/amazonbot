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
        price = price_tag.get_text(strip=True)
    except:
        price = "Fiyat alınamadı"

    try:
        rating_tag = soup.find("span", {"class": "a-icon-alt"})
        rating = rating_tag.get_text(strip=True).split(" ")[0]
    except:
        rating = "Puan alınamadı"

    try:
        comment_section = soup.find("div", {"id": "cm-cr-dp-review-list"})
        comments = comment_section.get_text(" ", strip=True) if comment_section else ""
        pos_score = comments.lower().count("excellent") + comments.lower().count("perfect")
        neg_score = comments.lower().count("terrible") + comments.lower().count("bad")
    except:
        pos_score, neg_score = 0, 0

    return {
        "name": title,
        "price": price,
        "rating": rating,
        "positive_mentions": pos_score,
        "negative_mentions": neg_score
    }
