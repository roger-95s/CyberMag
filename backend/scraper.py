# scraper.py
from bs4 import BeautifulSoup
import requests

def fetch_html(url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        
        return response.text

def extract_data(html: str, selectors: dict) -> dict:

        soup = BeautifulSoup(html, 'html.parser')

        # Extract urls
        url_tag = selectors['url_selector']['tag']
        url_class = selectors['url_selector']['class']
        url_items = soup.find_all(url_tag, class_=url_class, href=True)
        
        story_links = [link['href'] for link in url_items]
        if not story_links:
                print("❌ No story-link found")

        # Extract titles
        title_tag = selectors['title_selector']['tag']
        title_class = selectors['title_selector']['class']
        titles = soup.find_all(title_tag, class_=title_class)

        story_title = [title.text.strip() for title in titles]
        if not story_title:
                print("❌ No story-title found")

                

        return {
                'url': story_links,
                'title': story_title
        }