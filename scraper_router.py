from scraper_manager import get_scraper_for_url

def scrape_link(link):
    scraper = get_scraper_for_url(link)
    return scraper(link)
