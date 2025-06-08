from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product_from_amazon

app = Flask(__name__)

@app.route("/message", methods=["POST"])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if "amazon" in incoming_msg.lower():
        result = analyze_product_from_amazon(incoming_msg)
        msg = f"📦 {result['name']}\n💸 Fiyat: {result['price']}\n\n"

        for key, val in result["scores"].items():
            msg += f"✅ {key}: {val['value']} - {val['note']}\n"

        resp.message(msg)
    else:
        resp.message("🔎 Lütfen geçerli bir Amazon ürün linki gönderin.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
