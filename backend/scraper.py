# scraper.py
from bs4 import BeautifulSoup
import requests
from .tag_guide import list_of_sites

def fetch_html(url: str) -> str:
        try: 
                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/92.0.4515.159 Safari/537.36'
                }

                response = requests.get(url, headers=headers)
                response.raise_for_status()

        except NameError as e:
                print(f"❌ An error has occured: {e}")
        return response.text

for site in list_of_sites:
        url = site['url']
        html = fetch_html(url)
        if html:
                print("✅ Fetched HTML for", site['name'])
                print(f"✅ Fetch links: {site['url']}")

# Data extractor
def extract_data(html: str, selectors: dict) -> dict:

        soup = BeautifulSoup(html, 'html.parser')

        # Extract urls
        url_tag = selectors['url_selector']['tag']
        url_class = selectors['url_selector']['class']
        url_items = soup.find_all(url_tag, class_=url_class, href=True)
        
        print(f"{url_tag}")
        print(f"{url_class}")
        print(f"{url_items}")
        
        story_links = [link['href'] for link in url_items]
        if not story_links:
                print(f"❌ No story-link found: {url_items}")

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