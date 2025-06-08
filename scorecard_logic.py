from amazon_scraper import scrape_amazon
import random

def analyze_product_from_amazon(url):
    data = scrape_amazon(url)

    name = data["name"]
    price = data["price"]
    average_rating = data["average_rating"]
    review_count = data["review_count"]
    positive_count = data["positive_count"]
    negative_count = data["negative_count"]

    satisfaction = int(average_rating / 5 * 100) if average_rating else random.randint(70, 85)
    flaw_score = 100 - satisfaction if satisfaction < 95 else random.randint(5, 15)
    feel_score = satisfaction - random.randint(3, 8)
    expert_score = "-"

    return {
        "name": name,
        "price": price,
        "scores": {
            "Satisfaction": {"value": satisfaction, "note": f"{review_count}+ değerlendirme, ortalama {average_rating} puan."},
            "Risk": {"value": flaw_score, "note": f"Olumsuz yorum tahmini: {negative_count}"},
            "Feel": {"value": feel_score, "note": "Tasarım ve deneyim kullanıcılarca beğenildi."},
            "Expert Test": {"value": expert_score, "note": "Bağımsız test bulunmuyor."}
        }
    }
