from core import app
from scraper_manager import handle_scraping
from flask import request

@app.route("/scrape", methods=["POST"])
def scrape_link():
    data = request.get_json()
    link = data.get("link")
    result = handle_scraping(link)
    return result
