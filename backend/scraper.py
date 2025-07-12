"""Module providing a function python version."""

import traceback
import requests
from bs4 import BeautifulSoup

from .tag_guide import list_of_sites
from .models import save_report

# User-Agent header to mimic a browser request
# This is important to avoid being blocked by some websites that check for bots
# and to ensure we get the correct content.
# You can change this to any valid User-Agent string.
# For example, you can use a User-Agent from a real browser.
# Here is an example of a User-Agent string for Chrome on Windows 10.
# You can find more User-Agent strings at https://www.whatismybrowser.com/detect
# or https://developers.whatismybrowser.com/useragents/explore/
# or you can use a library like fake-useragent to generate random User-Agent strings.
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/92.0.4515.159 Safari/537.36"
    )
}


# Function to get the HTML content of a page
def get_response(page_url: str) -> BeautifulSoup | None:
    """Fetch and parse the HTML content of the given URL."""
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        return BeautifulSoup(response.text, "html.parser")
    except ImportError as e:
        print(f"❌ Failed to get {page_url}: Error type: {e}")
        return None


# Function to extract article titles and URLs from the soup object
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

        if not story_links:
            print(f"❌ No story-link found with selector: {url_class}")
            return {"title": [], "url": []}

        title_tag = selectors_map["title_selector"]["tag"]
        title_class = selectors_map["title_selector"]["class"]
        titles_items = soup_obj.find_all(title_tag, class_=title_class, limit=limit)

        story_titles = [title.get_text(strip=True) for title in titles_items]
        if not story_titles:
            print(f"❌ No story-title was found:{title_tag}{title_class}")
            return {"title": [], "url": []}

        return {
            "title": story_titles,
            "url": story_links,
        }

    except ImportError as e:
        print(f"❌ Error during fetching: {e}")
        traceback.print_exc()
        return {
            "title": "Unknown",
            "url": "Unknown",
        }


# Function to save articles to the database
def save_articles_to_db(articles_data: dict) -> int:
    """Save extracted articles to the database."""
    if (
        not articles_data
        or not articles_data.get("title")
        or not articles_data.get("url")
    ):
        return 0

    saved_count = 0
    titles = articles_data["title"]
    urls = articles_data["url"]
    min_length = min(len(titles), len(urls))

    for i in range(min_length):
        article_data = {
            "title": titles[i],
            "url": urls[i],
            "content": "",
            "summary": "",
            "risk_level": "",
        }
        save_report(report_data=article_data)
        saved_count += 1

    return saved_count


# 🔁 Main loop
for site in list_of_sites:
    name = site.get("name", "Unknown")
    url = site.get("url")
    selectors = site.get("selectors")

    if url and selectors:
        print(f"\n🔍 Processing: {name}")
        soup = get_response(url)

        if soup:
            data = fetch_data(soup, selectors, limit=10)

            if data.get("title") and data.get("url"):
                print(f"✅ {name}: {len(data['title'])} {len(data['url'])}")
                saved = save_articles_to_db(data)
                print(f"📦 Saved {saved} new articles to database")
            else:
                print(f"❌ No data scraped from {name}")
        else:
            print(f"❌ Could not get soup for {name}")
    else:
        print(f"⚠️ Skipping {name} — missing URL or selectors.")
