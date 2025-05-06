# scraper.py
import requests
from bs4 import BeautifulSoup
from tag_guide import TAG_GUIDE

def scrape_site(url, selectors):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.select_one(selectors['title'])
        content_tag = soup.select_one(selectors['content'])
        preview_tag = soup.select_one(selectors['preview'])

        return {
            "url": url,
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "content": content_tag.get_text(strip=True) if content_tag else None,
            "preview_link": preview_tag['href'] if preview_tag else None
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def scrape_all():
    results = []
    for site_url, selectors in TAG_GUIDE.items():
        print(f"Scraping: {site_url}")
        result = scrape_site(site_url, selectors)
        if result:
            results.append(result)
    return results















