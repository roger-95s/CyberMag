# scraper.py
from .tag_guide import list_of_sites
from bs4 import BeautifulSoup
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/92.0.4515.159 Safari/537.36'
}


# Get websites response
def get_response(url: dict):
        # Try to get a Web response
        try: 
                response = requests.get(url, headers=headers, timeout=10)
                print(f"✅ URL: {url} -> Status Code: {response.status_code} -> Datatype: {type(response)}") 
                # Soup sides
                return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
                print(f"❌ Failed to get {url}: Error type: {e}")
                return None


# URL Extractor
def fetch_data(soup: BeautifulSoup, selectors: dict) -> dict:  
        result = {}

        # Extract urls
        url_tag = selectors['url_selector']['tag']
        url_class = selectors['url_selector']['class']
        url_items = soup.find_all(url_tag, class_=url_class)

        story_links = [
                item.get('href') or item.find('a').get('href') 
                for item in url_items 
                if item.get('href') or (item.find('a') and item.find('a').get('href'))
]
        # story_links = [item.get('href') for item in url_items if item.get('href')]  # This work wiht the other website [item.find('a').get('href') for item in url_items if item.find('a')]
        if not story_links:
                print(f"❌ No story-link found with selector: {url_class}")  
        result['url'] = story_links

        # Extract titles
        title_tag = selectors['title_selector']['tag']
        title_class = selectors['title_selector']['class']
        titles_items = soup.find_all(title_tag, class_=title_class)

        story_title = [title.get_text(strip=True) for title in titles_items]
        if not story_title:
                print(f"❌ No story-title found with selector: {title_tag}{title_class}")
        result['title'] = story_title

        print(f'🤞 URLs:  {result["url"]}')
        print(f'🤞 TITLEs {result["title"]}')

        return result      


# Main loop
for site in list_of_sites:
        # Sites name's     
        name = site.get('name', 'Unknown')
        # Sites url's
        url = site.get('url')
        # Get Selector 
        selectors = site.get('selectors')
        # print(f'Site name\'s: {name}, Site url\'s: {url}, Site selectors: {selectors}')

        if url and selectors:
                print(f"\n🔍 Processing: {name}")
                soup = get_response(url)
                if soup:
                        data = fetch_data(soup, selectors)
                        print(f"✅ Scraped data from {name}: {len(data['title'])} titles, {len(data['url'])} URLs")
                else:
                        print(f"❌ Could not get soup for {name}")
        else:
                print(f"⚠️ Skipping site {name} due to missing URL or selectors.")

        