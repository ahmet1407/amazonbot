from openai_helper import generate_comment

def generate_scorecard(data):
    reviews = data["reviews"]

    prompt_satisfaction = f"Kullanıcı yorumlarına göre ürünün tatmin seviyesi yüksek mi? Kısaca açıkla:\n{reviews}"
    prompt_flaw = f"Bu yorumlara göre ürünle ilgili kusur veya risk var mı? Kısaca açıkla:\n{reviews}"
    prompt_aura = f"Yorumlara göre ürün hissiyatı ve tasarımı nasıl algılanıyor? Kısaca açıkla:\n{reviews}"

    return {
        "name": data["name"],
        "price": data["price"],
        "segment": data["segment"],
        "scores": {
            "satisfaction": {
                "score": 92,
                "comment": generate_comment(prompt_satisfaction)
            },
            "flaw": {
                "score": 14,
                "comment": generate_comment(prompt_flaw)
            },
            "aura": {
                "score": 88,
                "comment": generate_comment(prompt_aura)
            },
            "expert": {
                "score": data["expert_score"],
                "comment": "RTINGS testlerinde halı, düz zemin ve filtreleme performansı çok yüksek çıktı."
            }
        }
    }
