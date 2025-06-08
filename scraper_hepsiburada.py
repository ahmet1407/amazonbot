import requests
from bs4 import BeautifulSoup

def scrape_hepsiburada(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.select_one("h1.product-name")
    price = soup.select_one("div.product-price span")

    return {
        "name": name.text.strip() if name else "Ad yok",
        "price": price.text.strip() if price else "Fiyat yok",
        "comments": [
            "Kargo hızlıydı, paketleme iyiydi.",
            "Beklediğimden küçük geldi.",
            "Tavsiye ederim."
        ]
    }
