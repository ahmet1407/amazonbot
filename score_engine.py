import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_scorecard(product_data):
    comments = "\n".join(product_data["comments"])
    prompt = f"""Aşağıdaki ürün yorumlarını analiz et:
Ürün: {product_data['name']}
Yorumlar:
{comments}

Bu verilere göre:
- Tatmin puanı (100 üzerinden)
- Risk puanı (kusur/şikayet)
- Hissiyat (ürünün bıraktığı izlenim)
- Uzman değerlendirme puanı
- 2-3 cümlelik genel yorum

Sonuçları JSON olarak ver."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Bir ürün değerlendirme analistisin."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content

    import json
    scores = json.loads(reply)

    return {
        "name": product_data["name"],
        "price": product_data["price"],
        "segment": "Orta-Üst Seviye" if scores["Tatmin"] > 80 else "Ekonomik",
        "scores": {
            "satisfaction": {"score": scores["Tatmin"]},
            "flaw": {"score": scores["Risk"]},
            "aura": {"score": scores["Hissiyat"]},
            "expert": {"score": scores["Uzman değerlendirme puanı"]}
        },
        "summary": scores["Genel yorum"]
    }
