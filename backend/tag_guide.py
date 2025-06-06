"""
https://www.ransomware.live/,
https://cybersecurityventures.com/today/,
https://www.darkreading.com/,

, 'ListPreview-Title'
"""
# Global Dict/List 
list_of_sites = [
    {
        'name': 'The Hacker News',
        'url': 'https://thehackernews.com/',
        'selectors': {
                'url_selector': {'tag': 'a', 'class': 'story-link'},
                'title_selector': {'tag': 'h2', 'class': 'home-title'},
        }
    },
    {
        'name': 'DarkReading',
        'url': 'https://www.darkreading.com/',
        'selectors': {
                'url_selector': {'tag': 'a', 'class': 'ListPreview-Title'},
                'title_selector': {'tag': 'a', 'class': 'ListPreview-Title'},
        }
    },

    # Add more sites
]


