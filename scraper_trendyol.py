import requests
from bs4 import BeautifulSoup

def scrape_trendyol(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.select_one("h1.pr-new-br")
    price = soup.select_one("span.prc-dsc")

    return {
        "name": name.text.strip() if name else "Ad yok",
        "price": price.text.strip() if price else "Fiyat yok",
        "comments": [
            "Ürün anlatıldığı gibi.",
            "Kalite çok iyi ama fiyat yüksek.",
            "Beğendim, tavsiye ederim."
        ]
    }
