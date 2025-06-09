import re

def extract_scores(text):
    pattern = r"(Tatmin|Risk|Hissiyat|Uzman).*?(\d{1,3}).*?-\s*(.*)"
    results = re.findall(pattern, text, re.IGNORECASE)
    score_data = {}
    for category, score, comment in results:
        key = category.strip().lower()
        score_data[key] = {
            "score": int(score),
            "comment": comment.strip()
        }
    return score_data
