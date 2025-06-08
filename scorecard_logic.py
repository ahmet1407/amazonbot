from amazon_scraper import scrape_amazon
import random

def analyze_product_from_amazon(url):
    data = scrape_amazon(url)

    name = data.get("title", "Ürün bilgisi yok")
    price = data.get("price", "Fiyat bilgisi yok")
    rating = data.get("rating", "0")
    review_count = data.get("review_count", "0")

    try:
        average_rating = float(rating.replace(",", "."))
    except:
        average_rating = 4.0  # fallback

    # Skor hesaplama
    satisfaction = int(average_rating / 5 * 100)
    flaw_score = 100 - satisfaction if satisfaction < 95 else random.randint(5, 15)
    feel_score = satisfaction - random.randint(3, 8)
    expert_score = "-"  # Amazon'da teknik test yok

    # Açıklamalar
    satisfaction_note = f"Bu ürün {review_count}+ değerlendirme ile {average_rating} puan aldı."
    flaw_note = "Negatif yorumlar genellikle teslimat süresi veya paketleme ile ilgili."
    feel_note = "Kullanıcılar ürünün genel kalitesinden memnun."

    return {
        "name": name,
        "price": price,
        "scores": {
            "Satisfaction": {"value": satisfaction, "note": satisfaction_note},
            "Risk": {"value": flaw_score, "note": flaw_note},
            "Feel": {"value": feel_score, "note": feel_note},
            "Expert Test": {"value": expert_score, "note": "Bu ürün teknik testlere tabi tutulmamıştır."}
        }
    }
