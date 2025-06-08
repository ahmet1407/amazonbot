from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product_from_amazon

app = Flask(__name__)

@app.route("/message", methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if "amazon.com" in incoming_msg:
        result = analyze_product_from_amazon(incoming_msg)
        text = f"""📌 {result['name']}
💸 Fiyat: {result['price']}

✅ Tatmin: {result['scores']['Satisfaction']['value']} – {result['scores']['Satisfaction']['note']}
🧯 Risk: {result['scores']['Risk']['value']} – {result['scores']['Risk']['note']}
💠 Hissiyat: {result['scores']['Feel']['value']} – {result['scores']['Feel']['note']}
⚙️ Uzman Test: {result['scores']['Expert Test']['value']} – {result['scores']['Expert Test']['note']}
"""
    else:
        text = "Lütfen geçerli bir Amazon ürün linki paylaşın."

    resp.message(text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
