from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product_from_amazon

app = Flask(__name__)

@app.route("/message", methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()

    resp = MessagingResponse()

    if incoming_msg.startswith("http") and "amazon" in incoming_msg:
        try:
            result = analyze_product_from_amazon(incoming_msg)
            name = result["name"]
            price = result["price"]
            scores = result["scores"]

            reply = f"""📌 {name}
💸 {price}

### Skorlar (100 üzerinden)

✅ Tatmin: {scores['Satisfaction']['value']}
{scores['Satisfaction']['note']}

🧯 Risk: {scores['Risk']['value']}
{scores['Risk']['note']}

💠 Hissiyat: {scores['Feel']['value']}
{scores['Feel']['note']}

⚙️ Uzman Skoru: {scores['Expert Test']['value']}
{scores['Expert Test']['note']}
"""
        except Exception as e:
            reply = f"Ürün analiz edilirken bir hata oluştu: {e}"
    else:
        reply = "Lütfen geçerli bir Amazon ürün linki gönderin."

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
