def detect_platform(url: str) -> str:
    url = url.lower()
    if "amazon." in url:
        return "amazon"
    elif "hepsiburada.com" in url:
        return "hepsiburada"
    elif "trendyol.com" in url:
        return "trendyol"
    else:
        return "unknown"
