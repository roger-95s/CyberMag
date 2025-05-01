# URL of a trusted cybersecurity news site (can add more later)
# URL_SOURCE = [
#     "https://www.ransomware.live/",
#     "https://cybermap.kaspersky.com/",
#     "https://thehackernews.com/"


#     # Add more trusted sources here
# ] # Make this a list that can contain multiples URLs
# bodyPost = soup.find('div', class_='body-post clear') # This could be use on a llm tool to 
# url = soup.find('href', class_='story-link') 
# title = soup.find('h2', class_="home-title") & soup.find('h1', class_='story-title')
# articleBody = soup.find('article') or \
#             soup.find('div', class_='article-content') or \
#             soup.find('div', class_='post-content') or \
#             soup.find('div', {'id': 'content'}) or soup.find('vid', class_='articlebody clear cf')
# paragraph = soup.find_all('p', class_='articlebody')




# TAG_GUIDE ditc
TAG_GUIDE = {
    "https://www.ransomware.live/": {
        "title": "div.group_title",  
        "content": "div.bubble",
        "preview": "a.article-link"  
    },
    "https://www.kaspersky.com/": {
        "title": "h1.c-article__title",
        "content": "div.c-article__body p",
        "preview": "a.c-article__link" 
    },
    "https://thehackernews.com/": {
        "title": "h2.home-title",
        "content": "div.home-desc",
        "preview": "a.story-link"
    }
}