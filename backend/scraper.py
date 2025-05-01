# scraper.py
import requests
from bs4 import BeautifulSoup
from tag_guide import TAG_GUIDE

def scrape_site(url, selectors):
    """
    Fetches and parses a single site using the tag selectors.
    Returns a dict with title, content, and preview.
    """
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















# Fetcher function that fetch and handle content that will be use to store an Analyze 
# def fetch_latest_articles(limit=3):
#     """
#     Scrapes latest cybersecurity articles from NEWS_SOURCE using BeautifulSoup.
#     Returns a list of dictionaries: title, url, and content.
#     """

#     articles = []
#     try:
#         response = requests.get(URL_SOURCE)
#         soup = BeautifulSoup(response.text, "html.parser")
#         article_link = soup.find_all('a', class_='story-link', limit=limit)

#         for link in article_link:
#             # Identify the article Url, tittle, main content
#             url = link.get('href')
#             title = link.find('h2', class_='home-title').text.strip()    
            
#             articles.append({
#                 'url': url,
#                 'title': title
#             })        
#     except Exception as e:
#         print(f"Error accessing NEWS_SOURCE: {e}")
    
#     return articles

