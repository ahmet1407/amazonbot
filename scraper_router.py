from flask import Flask, request, jsonify, Response
from twilio.twiml.messaging_response import MessagingResponse
import traceback
import logging
from scraper_router import process_link_or_name

app = Flask(__name__)

# Logging ayarları
logging.basicConfig(filename="logs.txt", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/", methods=["GET"])
def index():
    return "Scorecard API Active"

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        sender = request.values.get("From", "")

        logging.info(f"Message received from {sender}: {incoming_msg}")

        if not incoming_msg:
            raise ValueError("Boş mesaj alındı.")

        scorecard = process_link_or_name(incoming_msg)

        if not scorecard:
            raise ValueError("Ürün bulunamadı veya analiz yapılamadı.")

        resp = MessagingResponse()
        msg = resp.message()
        msg.body(scorecard)

        logging.info(f"Scorecard gönderildi: {scorecard}")
        return Response(str(resp), mimetype="application/xml")

    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"Hata: {str(e)}\nTraceback: {error_trace}")

        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Üzgünüz, bir hata oluştu. Lütfen tekrar deneyin.")
        return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
