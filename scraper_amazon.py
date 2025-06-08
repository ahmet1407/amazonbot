import requests
from bs4 import BeautifulSoup

def scrape_amazon(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.select_one("#productTitle")
    price = soup.select_one(".a-price .a-offscreen")

    return {
        "name": name.text.strip() if name else "Ad yok",
        "price": price.text.strip() if price else "Fiyat yok",
        "comments": [
            "Çok sessiz çalışıyor.",
            "Pil ömrü biraz daha uzun olabilirdi.",
            "Tasarımı çok şık."
        ]
    }
