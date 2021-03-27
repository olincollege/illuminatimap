'''
Main code for the Illuminati Map project, our SoftDes Spring 2021 midterm.

Authors: Jacob Smilg and Markus Leschly
'''

import helpers
import datetime
from mediawiki import MediaWiki

wikipedia = MediaWiki(
    url='https://en.wikipedia.org/w/api.php',
    user_agent = 'illuminati-map',
    rate_limit = True,
    rate_limit_wait = datetime.timedelta(milliseconds=1000.0),
    cat_prefix = 'Category:')

billionaires = wikipedia.categorymembers("American_billionaires", results=None, subcategories=False)
billionaires = [title for title in billionaires if 'List of ' not in title] # remove non-person list entries

views = helpers.get_views(wikipedia, billionaires)
views = helpers.sort_dict(views, 20)

print(views)

titles = list(views.keys())
linkshere = helpers.get_linkshere(wikipedia, titles)
print(linkshere.keys())
common_links_dict = helpers.common_links(titles, linkshere)
print(common_links_dict)
# print(helpers.get_linkshere(wikipedia, titles), file=open("output.txt", 'w+'))