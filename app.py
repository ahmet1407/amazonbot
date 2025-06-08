from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product_from_amazon

app = Flask(__name__)

@app.route("/message", methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if "http" in incoming_msg and "amazon" in incoming_msg:
        try:
            result = analyze_product_from_amazon(incoming_msg)
            msg = f"""📌 {result['name']}
💸 Fiyat: {result['price']}

✅ Tatmin: {result['scores']['Satisfaction']['value']} - {result['scores']['Satisfaction']['note']}
🧯 Risk: {result['scores']['Risk']['value']} - {result['scores']['Risk']['note']}
💠 Hissiyat: {result['scores']['Feel']['value']} - {result['scores']['Feel']['note']}
⚙️ Uzman Testi: {result['scores']['Expert Test']['value']} - {result['scores']['Expert Test']['note']}
"""
        except Exception as e:
            msg = f"Ürün analiz edilemedi: {str(e)}"
    else:
        msg = "Lütfen Amazon ürün linki gönderin."

    resp.message(msg)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
