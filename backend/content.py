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
        print(f"🔍 Selector map structure: {selector_map}")
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
test_url = [
    {
        "name": "The Hacker News",
        "url": "https://thehackernews.com/2025/07/hackers-use-github-repositories-to-host.html",
    },
    {
        "name": "ThreatPost",
        "url": "https://threatpost.com/student-loan-breach-exposes-2-5m-records/180492/",
    },
]


# 🔁 Main loop
for i, (site, test_url) in enumerate(zip(list_of_sites, test_url)):
    # site contains selectors
    # url_data contains the actual URL to fetch
    selector = site.get("selectors", "Unknown")
    name = site.get("name", "Unknown")
    url = test_url.get("url", "Unknown")

    print(f"\n{'=' * 50}")
    # ===========================================================
    print(f"✅ Selectors found for site: {name}")
    print(f"Processing site {i + 1}/{len(list_of_sites)}")
    print(f"✅ Site_Url: {url}")

    # get site selectors from dictionary list (list_of_sites)
    if not selector:
        print("❌ Content_selector was not found:")
    else:
        selector.get("content_selector", {})
        # content_only = {"content_selector": selector.get("content_selector", {})}
        print(f"✅ Selectors_tags found: {selector}")

    soup = get_response(url)
    if not soup:
        print(print(f"❌ Could not get soup {url}"))
    else:
        data = fetch_content_data(soup, selector_map=selector)
        # print(data)
