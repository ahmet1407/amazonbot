from utils.serpapi_search import search_product_on_serpapi

def search_product(name):
    return search_product_on_serpapi(name)

# score_engine.py
from openai_helper import analyze_with_gpt
from score_utils import extract_scores

def generate_scorecard(product):
    prompt = f"""
Ürün adı: {product['name']}
Açıklama: {product['description']}
Kullanıcı Yorumları: {product['reviews']}

Lütfen aşağıdaki formatta puanlama yap:
Tatmin skoru (0-100) + kısa yorum,
Risk skoru (0-100) + kısa yorum,
Hissiyat skoru (0-100) + kısa yorum,
Uzman skoru (0-100) + kısa yorum.
"""
    gpt_output = analyze_with_gpt(prompt)
    scores = extract_scores(gpt_output)
    return {
        "name": product['name'],
        "price": product['price'],
        "scores": scores
    }
