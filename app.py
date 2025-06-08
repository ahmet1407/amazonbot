```python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product

app = Flask(__name__)

@app.route("/message", methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    try:
        result = analyze_product(incoming_msg)
        if result:
            reply = f"\n\U0001F4E6 {result['name']}\n\n\U0001F4B8 Fiyat: {result['price']}\n\n" \
                    + "\n".join([f"{k}: {v['value']}\n➔ {v['note']}" for k, v in result['scores'].items()])
        else:
            reply = "Bağlantı sağlanamadı veya veri alınamadı."
    except Exception as e:
        reply = f"Hata oluştu: {str(e)}"

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
```
