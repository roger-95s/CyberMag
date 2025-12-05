"""Scraper Module to fetch articles from various websites and store them in the database."""
import requests
from bs4 import BeautifulSoup
# --- IMPORTS FROM THE APP ---
from .models import WebsiteFetch, db


# Function to get the HTML content of a page
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/92.0.4515.159 Safari/537.36"
    )
}

def get_response(page_url: str) -> BeautifulSoup | None:
    """Fetch and parse the HTML content of the given URL."""
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None
    except Exception as e:
        print(f"❌ Failed to get {page_url}: {e}")
        return None

# Fetch function that scrape the areticles' meta data url, title  
def fetch_data(soup_obj: BeautifulSoup, selectors_map: dict, limit: int) -> dict:
    """Extract article titles and URLs using the provided selectors."""
    try:
        url_tag = selectors_map["url_selector"]["tag"]
        url_class = selectors_map["url_selector"]["class"]
        url_items = soup_obj.find_all(url_tag, class_=url_class, limit=limit)

        story_links = [
            item.get("href") or item.find("a").get("href")
            for item in url_items
            if item.get("href") or (item.find("a") and item.find("a").get("href"))
        ]

        title_tag = selectors_map["title_selector"]["tag"]
        title_class = selectors_map["title_selector"]["class"]
        titles_items = soup_obj.find_all(title_tag, class_=title_class, limit=limit)

        story_titles = [title.get_text(strip=True) for title in titles_items]

        return {
            "title": story_titles,
            "url": story_links,
        }
    except Exception as e:
        print(f"❌ Error during fetching: {e}")
        return {"title": [], "url": []}

# Function to save scraper article meta data 
def save_articles_to_db(articles_data, name: str) -> int:
    """Save extracted articles to the database."""
    
    # Validation
    if not articles_data or not articles_data.get("title") or not articles_data.get("url"):
        return 0

    site_name = name.strip()
    titles = articles_data.get("title", [])
    urls = articles_data.get("url", [])
    saved_count = 0

    print(f"🔖 Processing {len(urls)} articles for {site_name}...")

    # Loop through titles and URLs simultaneously
    for title, url in zip(titles, urls):
        try:
            # 1. Check if URL already exists to avoid duplicates
            existing_article = WebsiteFetch.query.filter_by(url=url).first()
            
            if not existing_article:
                # 2. Create the object with ACTUAL data
                new_article = WebsiteFetch(
                    site_name=site_name,
                    title=title,
                    url=url
                )
                
                # 3. Add to session
                db.session.add(new_article)
                saved_count += 1
            else:
                # Optional: Print skipped duplicates
                pass 

        except Exception as e:
            print(f"⚠️ Error preparing article {url}: {e}")

    # 4. Commit all new articles at once (Bulk commit)
    try:
        if saved_count > 0:
            db.session.commit()
            print(f"✅ Successfully saved {saved_count} new articles.")
        else:
            print("ℹ️ No new articles to save.")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Database Commit Error: {e}")
        return 0

    return saved_count

