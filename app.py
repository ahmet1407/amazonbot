from flask import Flask, request, jsonify, Response
from scraper_router import scrape_link
from score_engine import generate_scorecard
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_input = data.get('url') or data.get('query')

    if not product_input:
        return jsonify({"error": "Ürün linki ya da ismi gerekli."}), 400

    try:
        logging.info(f"🔍 Analyze isteği: {product_input}")
        product_data = scrape_link(product_input)
        logging.info(f"📦 Ürün verisi alındı: {product_data['name']}")
        scorecard = generate_scorecard(product_data)
        return jsonify(scorecard)
    except Exception as e:
        logging.exception("❌ Analyze hatası")
        return jsonify({"error": str(e)}), 500

@app.route('/message', methods=['POST'])
def message():
    data = request.form
    incoming_msg = data.get('Body', '').strip()
    logging.info(f"📩 Gelen mesaj: {incoming_msg}")

    try:
        product_data = scrape_link(incoming_msg)
        scorecard = generate_scorecard(product_data)

        msg = (
            f"📌 {scorecard['name']}\n"
            f"💸 {scorecard['price']}\n"
            f"✅ Tatmin: {scorecard['scores']['satisfaction']['score']} - {scorecard['scores']['satisfaction']['comment']}\n"
            f"🧯 Risk: {scorecard['scores']['flaw']['score']} - {scorecard['scores']['flaw']['comment']}\n"
            f"💠 Hissiyat: {scorecard['scores']['aura']['score']} - {scorecard['scores']['aura']['comment']}\n"
            f"⚙️ Uzman: {scorecard['scores']['expert']['score']} - {scorecard['scores']['expert']['comment']}"
        )
    except Exception as e:
        logging.exception("❌ WhatsApp mesajı hatası")
        msg = f"❌ Hata oluştu: {str(e)}"

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{msg}</Message>
</Response>"""
    return Response(twiml, mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
