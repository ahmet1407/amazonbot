from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from scorecard_logic import analyze_product
import os

app = Flask(__name__)

@app.route("/message", methods=['POST'])
def message():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    try:
        result = analyze_product(incoming_msg)
        reply = result
    except Exception as e:
        reply = f"Üzgünüm, ürün analiz edilirken bir hata oluştu: {str(e)}"

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
