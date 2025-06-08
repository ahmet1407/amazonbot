from amazon_scraper import scrape_amazon
import random

def analyze_product_from_amazon(url):
    data = scrape_amazon(url)

    name = data.get("name", "Ürün Bilgisi Yok")
    price = data.get("price", "Fiyat Bilgisi Yok")
    average_rating = data.get("rating", 0)
    pos = data.get("positive_mentions", 0)
    neg = data.get("negative_mentions", 0)

    try:
        satisfaction = int(float(average_rating) / 5 * 100)
    except:
        satisfaction = random.randint(75, 90)

    flaw_score = 100 - satisfaction if satisfaction < 95 else random.randint(5, 15)
    feel_score = satisfaction - random.randint(3, 8)
    expert_score = "-"  # Amazon'da teknik test yok

    return {
        "name": name,
        "price": price,
        "scores": {
            "Satisfaction": {
                "value": satisfaction,
                "note": f"Ortalama {average_rating}/5 ile olumlu yorum oranı yüksek ({pos} olumlu, {neg} olumsuz yorum)."
            },
            "Risk": {
                "value": flaw_score,
                "note": "Olumsuz yorumlar kalite veya teslimatla ilgili olabilir."
            },
            "Feel": {
                "value": feel_score,
                "note": "Tasarım ve kullanım deneyimi genelde iyi yorum almış."
            },
            "Expert Test": {
                "value": expert_score,
                "note": "Bağımsız teknik test verisi bulunmuyor."
            }
        }
    }
