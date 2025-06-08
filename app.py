from flask import Flask, request, jsonify, Response
from scraper_amazon import scrape_amazon
from score_engine import generate_scorecard

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message():
    data = request.form
    incoming_msg = data.get('Body')

    if "amazon.com.tr" in incoming_msg:
        try:
            product_data = scrape_amazon(incoming_msg)
            scorecard = generate_scorecard(product_data)
            msg = f"📌 {scorecard['name']}\n💸 {scorecard['price']}\n✅ Tatmin: {scorecard['scores']['satisfaction']['score']} - {scorecard['scores']['satisfaction']['comment']}\n🧯 Risk: {scorecard['scores']['flaw']['score']} - {scorecard['scores']['flaw']['comment']}\n💠 Hissiyat: {scorecard['scores']['aura']['score']} - {scorecard['scores']['aura']['comment']}\n⚙️ Uzman: {scorecard['scores']['expert']['score']}"
        except Exception as e:
            msg = f"❌ Hata oluştu: {str(e)}"
    else:
        msg = "❗ Lütfen geçerli bir Amazon.com.tr ürün linki gönderin."

    # Twilio'nun beklediği XML yanıt formatı (TwiML)
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{msg}</Message>
</Response>"""

    return Response(twiml_response, mimetype='application/xml')
