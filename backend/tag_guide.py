"""
https://www.ransomware.live/,
https://cybersecurityventures.com/today/,
https://www.darkreading.com/,

, 'ListPreview-Title'
"""

# Global Dict/List
list_of_sites = [
    {
        "name": "The Hacker News",
        "url": "https://thehackernews.com/",
        "selectors": {
            "url_selector": {"tag": "a", "class": "story-link"},
            "title_selector": {"tag": "h2", "class": "home-title"},
        },
    },
    {
        "name": "SecurityWeek",
        "url": "https://threatpost.com/",
        "selectors": {
            "url_selector": {"tag": "h2", "class": "c-card__title"},
            "title_selector": {"tag": "h2", "class": "c-card__title"},
        },
    },
    # Add more sites
]


"""
URL: https://threatpost.com/

Common structure:

    Titles: <h2 class="c-card__title">...</h2>

    Links: <a href="..." class="c-card__title-link">...</a>
"""
