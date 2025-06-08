from openai_helper import generate_comment
from product_compare import get_alternative_products

def generate_scorecard(data):
    reviews = data["reviews"]

    prompt_satisfaction = f"Bu kullanıcı yorumlarına göre ürün tatmin edici mi? Açıkla:\n{reviews}"
    prompt_flaw = f"Bu yorumlara göre ürünle ilgili risk/kusur var mı? Açıkla:\n{reviews}"
    prompt_aura = f"Yorumlara göre ürünün hissiyatı nasıl algılanıyor? Açıkla:\n{reviews}"

    scores = {
        "satisfaction": {
            "score": 90,
            "comment": generate_comment(prompt_satisfaction)
        },
        "flaw": {
            "score": 15,
            "comment": generate_comment(prompt_flaw)
        },
        "aura": {
            "score": 85,
            "comment": generate_comment(prompt_aura)
        },
        "expert": {
            "score": data["expert_score"],
            "comment": "Bağımsız testlerde genel performansı yüksek çıktı."
        }
    }

    return {
        "name": data["name"],
        "price": data["price"],
        "segment": data["segment"],
        "scores": scores,
        "alternatives": get_alternative_products(data["name"])
    }
