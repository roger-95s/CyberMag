# scraper.py
from .tag_guide import list_of_sites
from .models import Report, save_report
from bs4 import BeautifulSoup
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/92.0.4515.159 Safari/537.36'
}

result = {}

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
def fetch_data(soup: BeautifulSoup, selectors: dict, limit: int) -> dict:  
        try:
                # Extract urls
                url_tag = selectors['url_selector']['tag']
                url_class = selectors['url_selector']['class']
                url_items = soup.find_all(url_tag, class_=url_class, limit=limit)

                story_links = [
                        item.get('href') or item.find('a').get('href') 
                        for item in url_items 
                        if item.get('href') or (item.find('a') and item.find('a').get('href'))
                ]
                
                if not story_links:
                        print(f"❌ No story-link found with selector: {url_class}")  
                        return {"title": [], 'url': []}
                
                # Extract titles
                title_tag = selectors['title_selector']['tag']
                title_class = selectors['title_selector']['class']
                titles_items = soup.find_all(title_tag, class_=title_class, limit=limit)

                story_title = [title.get_text(strip=True) for title in titles_items]
                if not story_title:
                        print(f"❌ No story-title found with selector: {title_tag}{title_class}")
                        return {"title": [], 'url': []}
                # Debugging prints
                # print(f'🤞 URLs:  {result["url"]}')
                # print(f'🤞 TITLEs {result["title"]}')
                
                return {
                    "title": story_title,
                    "url": story_links,
                }
        
        except Exception as e:
                print(f"❌ Error during fetching: {e}")
        import traceback
        traceback.print_exc()
        return {
                "title": 'Unknown', 
                "url": 'Unknown',
        }

def save_articles_to_db(articles_data: dict) -> int:
  
    if not articles_data or not articles_data.get('title') or not articles_data.get('url'):
        return 0
    
    saved_count = 0
    titles = articles_data['title']
    urls = articles_data['url']
    min_length = min(len(titles), len(urls))
    
    for i in range(min_length):
        title = titles[i]
        url = urls[i]
        
        # Use your existing save_report function
        article_data = {
            "title": title,
            "url": url,
            "content": "",  # Will be filled later when analyzing individual articles
            "summary": "",
            "risk_level": ""
        }
        
        save_report(article_data)
        saved_count += 1
    
    return saved_count


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
                        data = fetch_data(soup, selectors, 10)  
                        if data and data.get('title') and data.get('url'):                     
                                print(f"✅ Scraped data from {name}: {len(data['title'])} titles, {len(data['url'])} URLs")
                                save_count = save_articles_to_db(data)
                                print(f'📦 Saved {save_count} new articles to database')
                        else:
                                print(f"❌ Not dara scraped form {name}")
                else:
                        print(f"❌ Could not get soup for {name}")                
        else:
                print(f"⚠️ Skipping site {name} due to missing URL or selectors.")

        