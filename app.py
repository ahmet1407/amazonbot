from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product_from_amazon

app = Flask(__name__)

@app.route("/message", methods=["POST"])
def message():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()

    if "amazon." in incoming_msg:
        try:
            result = analyze_product_from_amazon(incoming_msg)

            name = result.get("name", "Ürün adı alınamadı")
            price = result.get("price", "Fiyat bilgisi yok")
            scores = result.get("scores", {})

            reply = f"📌 *{name}*\n💸 Fiyat: {price}\n\n"
            for title, data in scores.items():
                reply += f"🔹 *{title}:* {data['value']} — _{data['note']}_\n"

        except Exception as e:
            reply = f"Ürün analiz edilirken hata oluştu: {str(e)}"
    else:
        reply = "Lütfen geçerli bir Amazon ürün linki gönderin."

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
