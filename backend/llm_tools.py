import os
import json
import requests 
from .scraper import fetch
from ollama import Client

# Step 1: Get HTML
html = fetch()

# Step 2: Prompt the LLM with both instruction + the HTML
prompt = f"""
Using the following HTML content:

{html}

Please search for each article URL and extract:
- URL: ...
- Title: ...
- Content: ...

Return the result as a JSON array where each item represents an article with the fields `url`, `title`, and `content`.
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
