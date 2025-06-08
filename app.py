from flask import Flask, request, jsonify, Response
from scraper_router import scrape_link
from score_engine import generate_scorecard

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_input = data.get('url') or data.get('query')

    if not product_input:
        return jsonify({"error": "Ürün linki ya da ismi gerekli."}), 400

    try:
        product_data = scrape_link(product_input)
        scorecard = generate_scorecard(product_data)
        return jsonify(scorecard)
    except Exception as e:
        print("❌ Analyze endpoint hatası:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/message', methods=['POST'])
def message():
    data = request.form
    incoming_msg = data.get('Body', '').strip()
    print("📩 Gelen mesaj:", incoming_msg)

    try:
        product_data = scrape_link(incoming_msg)
        scorecard = generate_scorecard(product_data)

        scores = scorecard.get('scores', {})
        msg = (
            f"📌 {scorecard.get('name', 'Ürün bulunamadı')}\n"
            f"💸 {scorecard.get('price', 'Fiyat yok')}\n"
            f"✅ Tatmin: {scores.get('satisfaction', {}).get('score', '—')} - {scores.get('satisfaction', {}).get('comment', '')}\n"
            f"🧯 Risk: {scores.get('flaw', {}).get('score', '—')} - {scores.get('flaw', {}).get('comment', '')}\n"
            f"💠 Hissiyat: {scores.get('aura', {}).get('score', '—')} - {scores.get('aura', {}).get('comment', '')}\n"
            f"⚙️ Uzman: {scores.get('expert', {}).get('score', '—')} - {scores.get('expert', {}).get('comment', '')}"
        )
    except Exception as e:
        print("❌ Message endpoint hatası:", str(e))
        msg = f"❌ Hata oluştu: {str(e)}"

    twiml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
    <Message>{msg}</Message>
</Response>"""
    return Response(twiml, mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
