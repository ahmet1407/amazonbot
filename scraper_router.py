from flask import request, jsonify
from app import app
from utils.detect_platform import detect_platform
from utils.scrape_amazon import scrape_amazon_product
from utils.scrape_hepsiburada import scrape_hepsiburada_product
from utils.serpapi_search import get_best_link_from_search
import logging

@app.route("/scrape", methods=["POST"])
def scrape_product():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing 'query' in request."}), 400

    try:
        if query.startswith("http://") or query.startswith("https://"):
            platform = detect_platform(query)
            if platform == "amazon":
                return scrape_amazon_product(query)
            elif platform == "hepsiburada":
                return scrape_hepsiburada_product(query)
            else:
                return jsonify({"error": f"Unsupported platform: {platform}"}), 400
        else:
            # Arama yapılmalı
            link = get_best_link_from_search(query)
            if not link:
                return jsonify({"error": "No product link found for the search."}), 404
            platform = detect_platform(link)
            if platform == "amazon":
                return scrape_amazon_product(link)
            elif platform == "hepsiburada":
                return scrape_hepsiburada_product(link)
            else:
                return jsonify({"error": f"Unsupported platform in search result: {platform}"}), 400

    except Exception as e:
        logging.exception("Unexpected error during scraping:")
        return jsonify({"error": str(e)}), 500
