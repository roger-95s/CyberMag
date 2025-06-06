# Add more links and do the same thing 
"""
https://www.ransomware.live/,
https://cybersecurityventures.com/today/,
https://www.darkreading.com/,

, 'ListPreview-Title'
"""
# Global Dict/List 
list_of_sites = [{
        'name': 'Hacker News',
        'url': 'https://thehackernews.com/',
        'selectors': {
                'url_selector': {'tag': 'a', 'class': 'story-link'},
                'title_selector': {'tag': 'h2', 'class': 'home-title'},
        }
}]
