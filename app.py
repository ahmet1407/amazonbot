import os
from flask import Flask, request, jsonify, Response
from scraper_router import scrape_link
from score_engine import generate_scorecard

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_url = data.get('url')

    if not product_url:
        return jsonify({"error": "Ürün linki gerekli."}), 400

    try:
        product_data = scrape_link(product_url)
        scorecard = generate_scorecard(product_data)
        return jsonify(scorecard)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/message', methods=['POST'])
def message():
    data = request.form
    incoming_msg = data.get('Body')
    print("🟡 Gelen mesaj:", incoming_msg)

    try:
        if any(domain in incoming_msg for domain in ["amazon.com", "amazon.com.tr", "hepsiburada.com", "trendyol.com"]):
            product_data = scrape_link(incoming_msg)
            print("🟢 Ürün verisi:", product_data)

            scorecard = generate_scorecard(product_data)
            print("🔵 Scorecard:", scorecard)

            # Ana mesaj – test sırasında istersen sadece msg = str(scorecard) yapabilirsin
            msg = f"""📌 {scorecard['name']}
💸 {scorecard['price']}
✅ Tatmin: {scorecard['scores']['satisfaction']['score']} - {scorecard['scores']['satisfaction']['comment']}
🧯 Risk: {scorecard['scores']['flaw']['score']} - {scorecard['scores']['flaw']['comment']}
💠 Hissiyat: {scorecard['scores']['aura']['score']} - {scorecard['scores']['aura']['comment']}
⚙️ Uzman: {scorecard['scores']['expert']['score']}
"""
        else:
            msg = "❗ Lütfen geçerli bir Amazon, Hepsiburada veya Trendyol linki gönderin."
    except Exception as e:
        print("🔴 HATA:", str(e))
        msg = f"❌ Hata oluştu: {str(e)}"

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{msg}</Message>
</Response>"""

    return Response(twiml_response, mimetype='application/xml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
