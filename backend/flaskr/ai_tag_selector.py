from .scraper import soup
from ollama import Client




# Building a AI agent that can scraper for tags selectors, to be use to scrape articles from a webpage

# Step 1: Get HTML
html = soup

# Step 2: Prompt the LLM with both instruction + the HTML
prompt = f"""
Using the following HTML content:

{html}

Please search for each article URL and extract:
# Extract titles
        title_tag = selectors['title_selector']['tag']
        title_class = selectors['title_selector']['class']
        titles = soup.find_all(title_tag, class_=title_class)
# Extract urls
        url_tag = selectors['url_selector']['tag']
        url_class = selectors['url_selector']['class']
        url_items = soup.find_all(url_tag, class_=url_class, href=True)

  return :
    'url': ,
    'title:

"""


