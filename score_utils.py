def calculate_satisfaction_score(reviews):
    if not reviews:
        return 50
    positive_reviews = [r for r in reviews if r['rating'] >= 4]
    return round((len(positive_reviews) / len(reviews)) * 100, 2)

def calculate_flaw_score(reviews):
    if not reviews:
        return 50
    negative_reviews = [r for r in reviews if r['rating'] <= 2]
    return round((len(negative_reviews) / len(reviews)) * 100, 2)

def calculate_aura_score(title, image_url):
    base_score = 60
    if any(keyword in title.lower() for keyword in ['premium', 'deluxe', 'gold']):
        base_score += 10
    if image_url and ('webp' in image_url or 'highres' in image_url):
        base_score += 10
    return min(base_score, 100)

def normalize_rating(rating, max_rating=5):
    return round((rating / max_rating) * 100, 2)
