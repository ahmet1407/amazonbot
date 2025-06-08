from flask import Flask, request, Response
import os
from product_search import search_product_url
from scraper_router import scrape_link
from score_engine import generate_scorecard

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    incoming_msg = request.form.get('Body', '').strip()
    print("📩 Gelen mesaj:", incoming_msg)

    if not incoming_msg:
        return respond("Lütfen bir ürün ismi girin.")

    try:
        product_url = search_product_url(incoming_msg)
        if not product_url:
            return respond("🔍 Ürün bulunamadı. Daha açık bir isim deneyin.")

        product_data = scrape_link(product_url)
        scorecard = generate_scorecard(product_data)

        msg = (
            f"📌 {scorecard['name']}\n"
            f"💸 {scorecard['price']}\n"
            f"🏆 {scorecard.get('segment', 'Segment bilgisi yok')}\n\n"
            f"✅ Tatmin: {scorecard['scores']['satisfaction']['score']}\n"
            f"🧯 Risk: {scorecard['scores']['flaw']['score']}\n"
            f"💠 Hissiyat: {scorecard['scores']['aura']['score']}\n"
            f"⚙️ Uzman Skoru: {scorecard['scores']['expert']['score']}\n\n"
            f"✍️ {scorecard['summary']}"
        )
    except Exception as e:
        msg = f"❌ Hata: {str(e)}"

    return respond(msg)

def respond(message):
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response><Message>{message}</Message></Response>"""
    return Response(twiml, mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
