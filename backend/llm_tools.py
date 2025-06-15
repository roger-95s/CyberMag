from html.entities import html5
import os
import json
import requests 
from bs4 import BeautifulSoup
from .scraper import soup
from ollama import Client

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

client = Client(host='http://localhost:11434')

response = client.chat(model='llama3.2:latest', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

# print(type(f'✅ {response}'))        # See what kind of object it is
# print(f'🤞 {response}')              # See what it looks like
print(f'🎲 Raw HTML input (optional): {html}')
# Step 4: Get result 
print(f"🤞 {response['message']['content']}")
