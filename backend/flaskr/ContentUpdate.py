"""
modify content scraper to pass 3 articles simultaneously to be analyze for each model.  
after save full content site _name, title, ai_output. 
Deleted the article title and url that was analyzed form the ai tool. 
"""
from .models import db, WebsiteFetch
from .tag_guide import list_of_sites

# Query 3 article from The Hacker News and return a dictionary list of articles
def site_separated_by_name(): 
    # Query sita metadata from database 
    articles_metadata = db.session.execute(db.select(WebsiteFetch).order_by(WebsiteFetch.site_name).limit(3)).scalars()

    # loop the data and store in to list [] variable  
    li = [a.to_dict() for a in articles_metadata]

    # return the list data
    return li


def tags_selectors():

    for list_tag in list_of_sites:
        li = [list_tag.get('name'), list_tag.get('selectors')]

        if li:
            if 'The Hacker News' in li:
                selectors = list_tag
        else:
            print("error")
    
    return selectors