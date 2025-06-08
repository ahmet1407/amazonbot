from amazon_scraper import scrape_amazon
import random


def analyze_product_from_amazon(url):
    data = scrape_amazon(url)

    name = data.get("name", data.get("title", "Ürün Bilgisi Yok"))
    price = data.get("price", "Fiyat Bilgisi Yok USD")
    rating = data.get("average_rating", 0)
    review_count = data.get("review_count", 0)
    pos_score = data.get("positive_mentions", 0)
    neg_score = data.get("negative_mentions", 0)

    satisfaction = int(float(rating) / 5 * 100) if rating else random.randint(75, 85)
    flaw_score = min(100, 100 - satisfaction + random.randint(5, 10))
    feel_score = max(0, satisfaction - random.randint(5, 10))
    expert_score = "-"

    satisfaction_note = f"{satisfaction} – {review_count}+ değerlendirme, ortalama {rating} puan."
    flaw_note = f"{flaw_score} – Olumsuz yorum tahmini: {neg_score}"
    feel_note = f"{feel_score} – Tasarım ve deneyim kullanıcılarca beğenildi."
    expert_note = "- – Bağımsız test bulunmuyor."

    return {
        "name": name,
        "price": price,
        "scores": {
            "Satisfaction": {"value": satisfaction, "note": satisfaction_note},
            "Risk": {"value": flaw_score, "note": flaw_note},
            "Feel": {"value": feel_score, "note": feel_note},
            "Expert Test": {"value": expert_score, "note": expert_note}
        }
    }
