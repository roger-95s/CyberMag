"""
content fetch articles' content from sites and save them to the database.
This script uses BeautifulSoup to parse HTML and extract articles' content.
It iterates over a predefined list of sites, fetches the HTML content,
extracts the required data, and saves it to the database.
"""

import traceback
import requests
from bs4 import BeautifulSoup

# import save_report
from .tag_guide import list_of_sites

# Impport artile get_all_reports(url)
from .models import get_all_reports

# Get a request from webpage
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
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get {page_url}: Error type: {e}")
        return None
    except ImportError as e:
        print(f"❌ Failed to get {page_url}: Error type: {e}")
        return None


# fetch for articles content_selector tags
def fetch_content_data(soup_obj: BeautifulSoup, selector_map: dict):
    """fetch articles' content using the provided selectors"""
    try:
        # print(f"🔍 Selector map structure: {selector_map}")
        # check if content_selector exists
        if "content_selector" not in selector_map:
            print("❌ 'content_selector' key not found in selector_map")
            return {"content": []}

        # Extract selector components safely
        content_tag = selector_map["content_selector"]["tag"]
        content_ancestor_tag = selector_map["content_selector"]["ancestor_tag"]
        content_class = selector_map["content_selector"]["ancestor_class"]
        ancestor_containers = soup_obj.find_all(
            content_ancestor_tag, class_=content_class
        )

        # print(
        #     f"Found {len(ancestor_containers)} ancestor containers with class '{content_class}'"
        # )

        content_items = []
        for container in ancestor_containers:
            items = container.find_all(content_tag)
            content_items.extend(items)
            # print(f"📦{container}")

        # print(
        #     f"Found {len(content_items)} {content_tag} tags within ancestor containers"
        # )

        contents = []
        for content in content_items:
            text = content.get_text(strip=True)
            # print(
            #     f"Content text: {text[:100]}..."
            #     if len(text) > 100
            #     else f"Content text: {text}"
            # )
            if text:
                contents.append(text)
        if not contents:
            return {"content": []}

        return {"content": contents}

    except ImportError as e:
        print(f"❌ Error during fetching article content: {e}")
        traceback.print_exc()
        return {"content": []}


# Save in data base refere articles content by id to articles fetched on scraper.py
# Debug function to inspect the selector structure
def debug_selector():
    """Debug function to inspect the imported selectors"""
    # print("🔍 Debugging selector structure...")
    # print(f"Number of sites in list_of_sites: {len(list_of_sites)}")

    # for i, site in enumerate(list_of_sites):
    #     print(f"\n📍Site {i+1}: {site.get('name')}")
    #     if "selectors" in site:
    #         print(f" Selectors: {site['selectors'].get('content_selector')}")
    #     else:
    #         print(" ❌ No selectors found")


# Run debug
debug_selector()


# Connect the databse cybermag.db en stract each url
# Make sure that each link is pair with it site selectors.
test_url = get_all_reports()

# Build a quick lookup dictionary from list_of_sites
site_lookup = {site["name"]: site for site in list_of_sites}

# 🔁 Main loopIterate over all DB articles
for i, row in enumerate(test_url, start=1):
    name = row.get("site_name", "Unknown")
    url = row.get("url", "Unknown")

    print(f"\n{'=' * 50}")
    print(f"✅ Site: {name}")
    print(f"Processing article {i}/{len(test_url)}")
    print(f"✅ Site_Url: {url}")

    # Get selectors by site name
    site = site_lookup.get(name)
    if not site:
        print(f"❌ No selectors found for site '{name}'")
        continue

    selector = site.get("selectors", {})
    if not selector:
        print("❌ Content_selector was not found:")
        continue

    # Fetch and parse
    soup = get_response(url)
    if not soup:
        print(f"❌ Could not get soup for {url}")
        continue

    data = fetch_content_data(soup, selector_map=selector)
    print(data)
