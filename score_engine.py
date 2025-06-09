from openai_helper import generate_comment

def generate_scorecard(product_data):
    reviews = product_data.get("reviews") or []

    def score_and_comment(prompt_prefix):
        joined = " | ".join(reviews)
        prompt = f"{prompt_prefix}: {joined}"
        print("🧠 GPT Prompt:", prompt)  # Debug log

        comment = generate_comment(prompt)
        print("🧠 GPT Yorum:", comment)  # Debug log

        score = 80 + len(joined) % 15
        return {"score": score, "comment": comment}

    return {
        "name": product_data["name"],
        "price": product_data["price"],
        "scores": {
            "satisfaction": score_and_comment("Kullanıcı memnuniyeti"),
            "flaw": score_and_comment("Negatif yorumlara göre risk analizi"),
            "aura": score_and_comment("Ürünün verdiği his ve tasarım algısı"),
            "expert": {
                "score": product_data.get("expert_score", 88),
                "comment": "Bağımsız testlerden alınan teknik puan"
            }
        }
    }
