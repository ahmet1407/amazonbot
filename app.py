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
    incoming_msg = data.get('Body', '').strip()
    print("📩 Gelen mesaj:", incoming_msg)

    msg_lower = incoming_msg.lower()
    if any(domain in msg_lower for domain in ["amazon", "amzn.eu", "hepsiburada", "trendyol"]):
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
            print("❌ Hata:", str(e))
            msg = f"❌ Hata oluştu: {str(e)}"
    else:
        msg = "❗ Amazon, Hepsiburada veya Trendyol linki gönder."

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{msg}</Message>
</Response>"""

    return Response(twiml, mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
