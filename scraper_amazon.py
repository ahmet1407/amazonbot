import os
import requests

def scrape_amazon(input_text):
    if input_text.startswith("http"):
        # Gerçek linkle sahte veri (test amaçlı)
        return {
            "name": "Duracell CR2032 Pil",
            "price": "149 TL",
            "segment": "Ekonomik",
            "reviews": ["Fiyat/performans ürünü", "Hızlı geldi", "Pil kutusu sağlam"],
            "expert_score": 78
        }
    else:
        # Yazıyla gelen örnek
        return {
            "name": "Dyson V15 Detect",
            "price": "18.999 TL",
            "segment": "Premium",
            "reviews": ["Çekim gücü çok iyi", "Tozları görünce mutlu oldum", "Kablo derdi yok"],
            "expert_score": 94
        }
