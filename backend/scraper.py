# scraper.py
from .tag_guide import list_of_sites
from bs4 import BeautifulSoup
import requests


html = []

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/92.0.4515.159 Safari/537.36'
}


# URL Extractor
def fetch_data(html: str, selectors: dict) -> dict:  
        
        # Extract urls
        url_tag = selectors['url_selector']['tag']
        url_class = selectors['url_selector']['class']
        url_items = html.find_all(url_tag, class_=url_class)

        story_links = [item.find('a').get(' href') for item in url_items if item.find('a')]
        if not story_links:
                print(f"❌ No story-link found with selector: {url_tag}.{url_class}")   
        # Extract titles
        title_tag = selectors['title_selector']['tag']
        title_class = selectors['title_selector']['class']
        titles_items = html.find_all(title_tag, class_=title_class)     
        story_title = [title.get_text(strip=True) for title in titles_items]
        if not story_title:
                print(f"❌ No story-title found with selector: {title_tag}{title_class}")

        return {
                'url': story_links,
                'title': story_title
        }


# Get websites response
def get_response(url: dict):
        # Try to get a Web response
        try: 
                response = requests.get(url, headers=headers, timeout=10)
                print(f"✅ URL: {url} -> Status Code: {response.status_code} -> Datatype: {type(response)}") 
                # Soup sides
                try: 
                        soup = BeautifulSoup(response.text, 'html.parser') 
                        print(f'DataType of soup Var: {type(soup)}')
                        # print(soup.prettify())
                        return html.append(soup)
                except Exception as e:
                        print(f"❌ Exaction error just ocurre, soup wasn't allow: {e}")
                return None
        except requests.RequestException as e:
                print(f"❌ Failed to get {url}: Error type: {e}")
                return None
        
              

# Main loop
for site in list_of_sites:
        url = site.get('url')
        # print(type(url))
        if url:
                get_response(url) 
        else:
                print(f"No URL found for site: {site.get('name', 'Unknown')}")


