'''
Data acquisition code for the Illuminati Map project, our SoftDes Spring 2021 midterm.

Authors: Jacob Smilg and Markus Leschly
'''

from helpers import common_links
import sys
import pickle
import argparse
from datetime import timedelta, datetime
from mediawiki import MediaWiki


DEFAULT_CATEGORY = 'American_billionaires'
DEFAULT_RATE_LIMIT = True
DEFAULT_RATE_LIMIT_WAIT = 1.0   # seconds
SSN = '907-64-8942' #   ;)

GENERAL_SEARCH_PARAMS = {
    'format': 'json',
    'formatversion': 2,
    'redirects': 1,
    'gcmnamespace': 0,  # article pages only
    'gcmlimit': 500,
    'prop': 'pageviews|linkshere',
    'generator': 'categorymembers',
    'pvipdays': 60,
    'lhnamespace': 0,   # article pages only
    'lhlimit': 500,
    }

def get_generator(wiki, category):
    search_params = {
        'gcmtitle': f'Category:{category}',
    }

    search_params.update(GENERAL_SEARCH_PARAMS)
    print(f'Getting information for category: {category}...')
    pages = []
    finished = False
    cont = dict()

    start_time = datetime.now()
    last_update = timedelta(seconds=1)
    requests_count = 1

    while not finished:
        params = search_params.copy()
        params.update(cont)
        result = wiki.wiki_request(params)
        pages.extend(result['query']['pages'])

        elapsed_time = datetime.now() - start_time
        elapsed_time_str = str(elapsed_time).split('.')[0]

        # continue if we need to
        if result.get('continue', False):
            cont = result['continue']
            
            # progress message
            if elapsed_time - last_update > timedelta(seconds=1):
                print(f'[{elapsed_time_str}]   Sending request #{requests_count}...'.ljust(80), end='\r', flush=True)                
                last_update = elapsed_time
                requests_count += 1
        else:
            print(f'[{elapsed_time_str}]   Done getting data!'.ljust(80))
            finished = True
    
    return pages

def format_data(data):
    print('Formatting data...')
    formatted_data = {}
    for page in data:
        title = page['title']
        if 'List of' in title:
            continue
        if not formatted_data.get(title, False):
            # make a new entry for the category member
            formatted_data[title] = {'linkshere': [],'pageviews': {}}
            formatted_data[title]['pageid'] = page['pageid']
        # add to the category member's entry
        if page.get('linkshere', False):
            formatted_data[title]['linkshere'].extend([linkpage['title'] for linkpage in page['linkshere']])
        if page.get('pageviews', False):
            formatted_data[title]['pageviews'].update(page['pageviews'])
    for page in formatted_data.keys():
        page_views = {date: views for date, views in formatted_data[page]['pageviews'].items() if views is not None}
        formatted_data[page]['total_views'] = sum(list(page_views.values()))
    print('Finding common links...')
    formatted_data = common_links(formatted_data)
    print('Done formatting data!')
    return formatted_data

def get_data(category, rate_limit, rate_limit_wait):
    wikipedia = MediaWiki(
        url='https://en.wikipedia.org/w/api.php',
        user_agent = 'illuminati-map',
        rate_limit = rate_limit,
        rate_limit_wait = timedelta(seconds=rate_limit_wait),
        cat_prefix = 'Category:')

    raw_data = get_generator(wikipedia, category)
    return format_data(raw_data)

def get_parser(name):
    '''
    Return the command-line argument parser used for this script.

    Borrowed from recursive_art.py from assignment 3.

    Args:
        name: A string representing the name of the script.

    Returns:
        An argparse namespace representing the successfully parsed arguments'
        names and values.
    '''

    parser = argparse.ArgumentParser(name)
    parser.add_argument('filename', type=str, help='Path to save the obtained data (.pkl) to')
    parser.add_argument('--category', type=str, default=DEFAULT_CATEGORY,
                        help=f'Width of the generated image in pixels (default: {DEFAULT_CATEGORY})')
    parser.add_argument('--rate-limit', type=bool, default=DEFAULT_RATE_LIMIT,
                        help='Use rate limiting to limit calls to Wikipedia '
                            f'(default: {DEFAULT_RATE_LIMIT})')
    parser.add_argument('--rate-limit-wait', type=bool, default=DEFAULT_RATE_LIMIT_WAIT,
                        help='The amount of time to wait between requests in seconds '
                            f'(default: {DEFAULT_RATE_LIMIT_WAIT})')
    return parser

def main(args):
    parser = get_parser(args[0])
    parsed_args = parser.parse_args(args[1:])
    data = get_data(parsed_args.category, parsed_args.rate_limit,
                    parsed_args.rate_limit_wait)
    with open(parsed_args.filename, 'wb') as file:
        pickle.dump(data, file)

if __name__ == '__main__':
    main(sys.argv)
