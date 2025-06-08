from flask import Flask, request, jsonify
from scraper_amazon import scrape_amazon
from score_engine import generate_scorecard

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    product_url = data.get('url')
    
    if not product_url:
        return jsonify({"error": "Ürün linki gerekli."}), 400

    try:
        product_data = scrape_amazon(product_url)
        scorecard = generate_scorecard(product_data)
        return jsonify(scorecard)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
