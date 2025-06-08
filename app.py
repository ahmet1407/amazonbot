from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product_from_any_link

app = Flask(__name__)

@app.route("/message", methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    if incoming_msg.startswith("http"):
        try:
            result = analyze_product_from_any_link(incoming_msg)

            name = result.get("name", "Ürün Bilgisi Yok")
            price = result.get("price", "Fiyat Bilgisi Yok")
            scores = result.get("scores", {})

            reply = f"📌 {name}\n💸 {price}\n"
            for key, val in scores.items():
                reply += f"\n✅ {key}: {val['value']}\n{val['note']}\n"
        except Exception as e:
            reply = f"Hata oluştu: {e}"
    else:
        reply = "Lütfen geçerli bir ürün bağlantısı gönderin."

    resp.message(reply)
    return str(resp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
