# scraper.py
from bs4 import BeautifulSoup
import requests

# Add more links and do the same thing 
"""
https://www.ransomware.live/,
https://cybersecurityventures.com/today/,
https://www.darkreading.com/,

, 'ListPreview-Title'
"""
# Global Dict/List 
list_of_sites = {
        'name': 'Hacker News',
        'url': 'https://thehackernews.com/',
        'selectors': {
                'url_selector': {'tag': 'a', 'class': 'story-link'},
                'title_selector': {'tag': 'h2', 'class': 'home-title'},
        }
}

WEB_URL = "https://thehackernews.com/"  
        

def scraper() -> dict:
        try:
                # Sent a Get request 
                response = requests.get(WEB_URL)
                response.raise_for_status() # Raise HTTPError for bad responses
                # Parse the HTML content 
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract data 
                url_item = soup.find_all('a', class_=['story-link'], href=True) 
                story_links = [link['href'] for link in url_item]
                if not story_links:
                        print("❌ No story-link found")  
                
                titles = soup.find_all('h2', class_='home-title')
                story_title = [title.text.strip() for title in titles]
                if not story_title:
                        print("❌ No story-title found")   

        except requests.exceptions.RequestException as e:
                print(f"❌ Unexpected Request error while get(Weburl): {e}")
        except Exception as e:
                print(f"❌ Error: occurred: {e}")
                return None
        
        # print(f'😁 {soup.prettify()}')

        return {
                'url': story_links,
                'title': story_title,
        }

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