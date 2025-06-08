from flask import Flask, request, jsonify
from scraper_amazon import scrape_amazon
from score_engine import generate_scorecard

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_url = data.get('url')

    if not product_url:
        return jsonify({"error": "Ürün linki gerekli."}), 400

    try:
        product_data = scrape_amazon(product_url)
        scorecard = generate_scorecard(product_data)
        return jsonify(scorecard)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/message', methods=['POST'])
def message():
    data = request.form  # Twilio, JSON değil form-data gönderir
    incoming_msg = data.get('Body')

    if "amazon.com.tr" in incoming_msg:
        try:
            product_data = scrape_amazon(incoming_msg)
            scorecard = generate_scorecard(product_data)
            msg = f"📌 {scorecard['name']}\n💸 {scorecard['price']}\n✅ Tatmin: {scorecard['scores']['satisfaction']['score']} - {scorecard['scores']['satisfaction']['comment']}\n🧯 Risk: {scorecard['scores']['flaw']['score']} - {scorecard['scores']['flaw']['comment']}\n💠 Hissiyat: {scorecard['scores']['aura']['score']} - {scorecard['scores']['aura']['comment']}\n⚙️ Uzman: {scorecard['scores']['expert']['score']}"
        except Exception as e:
            msg = f"❌ Hata oluştu: {str(e)}"
    else:
        msg = "❗ Lütfen geçerli bir Amazon.com.tr ürün linki gönderin."

    return msg, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
