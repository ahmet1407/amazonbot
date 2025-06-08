@app.route('/message', methods=['POST'])
def message():
    from scraper_router import scrape_link
    from score_engine import generate_scorecard
    from flask import Response

    data = request.form
    incoming_msg = data.get('Body', '').strip()
    print("📩 Gelen mesaj:", incoming_msg)

    # Basit domain kontrolü
    msg_lower = incoming_msg.lower()
    if "amazon" in msg_lower or "amzn.eu" in msg_lower or "hepsiburada" in msg_lower or "trendyol" in msg_lower:
        try:
            product_data = scrape_link(incoming_msg)
            scorecard = generate_scorecard(product_data)

            # Sadece 2 satırlık, sade yanıt
            msg = (
                f"{scorecard['name']} – {scorecard['price']}\n"
                f"✅ Tatmin: {scorecard['scores']['satisfaction']['score']} / "
                f"🧯 Risk: {scorecard['scores']['flaw']['score']}"
            )
        except Exception as e:
            msg = f"❌ Hata oluştu: {str(e)}"
    else:
        msg = "❗ Lütfen Amazon, Hepsiburada veya Trendyol linki gönderin."

    # Kısa XML cevabı
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>{msg}</Message>
</Response>"""

    return Response(twiml_response, mimetype="application/xml")
