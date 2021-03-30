'''
Data acquisition code for the Illuminati Map project, our SoftDes Spring 2021 midterm.

Authors: Jacob Smilg and Markus Leschly
'''

import sys
import pickle
import math
import argparse
import datetime
import time
from mediawiki import MediaWiki
from tqdm import tqdm
import helpers


DEFAULT_CATEGORY = 'American_billionaires'
DEFAULT_RATE_LIMIT = True
DEFAULT_RATE_LIMIT_WAIT = 1.0   # seconds

GENERAL_SEARCH_PARAMS = {
    'format': 'json',
    'formatversion': 2,
    'redirects': 1
    }

def get_views(wiki, cat_members, progress_bar=False):
    search_params = {
        'prop': 'pageviews',
        'pvipdays': 60
    }
    search_params.update(GENERAL_SEARCH_PARAMS)

    views = {cat_member: 0 for cat_member in cat_members}

    # get a list of groups of 50 category members
    cat_member_groups = ('|'.join(list(filter(None, chunk)))
                            for chunk in helpers.grouper(cat_members, 50))

    # create progress bar/iterable
    _iterable = tqdm(
        cat_member_groups,
        disable=(not progress_bar),
        desc='Page view requests',
        unit='requests',
        total=math.ceil(len(cat_members)/50)
        )

    # can only get 50 pages at a time
    for request_titles in _iterable:
        cont = dict()
        finished = False
        # api has a "continue" thing that happens if there's too much data
        while not finished:
            params = search_params.copy()
            params.update(cont)
            params['titles'] = request_titles
            result = wiki.wiki_request(params)
            for page in result['query']['pages']:
                total_views = sum([view for view in list(page['pageviews'].values())
                                    if view is not None])
                views[page['title']] += total_views

            # continue if we need to
            if result.get('continue', False):
                cont = result['continue']
                # search_params.update(result['continue'])
            else:
                cont = dict()
                finished = True
        # reset continue params so next requests don't break
        # search_params.update({'pvipcontinue': '', 'continue': ''})

    return views

def get_linkshere(wiki, cat_members, progress_bar=False):
    search_params = {
        'prop': 'linkshere',
        'lhnamespace': 0,
        'lhlimit': 500,
    }
    search_params.update(GENERAL_SEARCH_PARAMS)
    
    linkshere = {cat_member: [] for cat_member in cat_members}

    # get a list of groups of 50 category members
    cat_member_groups = ('|'.join(list(filter(None, chunk)))
                            for chunk in helpers.grouper(cat_members, 50))

    _iterable = tqdm(
        cat_member_groups,
        disable=(not progress_bar),
        desc='Page links requests',
        unit='requests',
        total=math.ceil(len(cat_members)/50)
        )
    
    for request_titles in _iterable:
        cont = dict()
        finished = False
        while not finished:
            params = search_params.copy()
            params.update(cont)
            # get data for group from API
            params['titles'] = request_titles
            result = wiki.wiki_request(params)
            for page in result['query']['pages']:
                # linkshere doesn't exist if no pages link to the given page, so make sure it exists
                # before trying to reference it.
                if page.get('linkshere', False):
                    # put links in dictionary
                    for linker in page['linkshere']:
                        linkshere[page['title']].append(linker['title'])

            # continue if we need to
            if result.get('continue', False):
                cont = result['continue']
            else:
                cont = dict()
                finished = True
        # search_params.update({'pvipcontinue': '', 'continue': ''})

    return linkshere

def common_links(names, links_dict):
    common_links_dict = {name: [] for name in names}
    for name in names:
        for linker in links_dict[name]:
            if linker in names:
                common_links_dict[name].append(linker)
    return common_links_dict

def get_data(category, num_pages, rate_limit, rate_limit_wait):
    wikipedia = MediaWiki(
        url='https://en.wikipedia.org/w/api.php',
        user_agent = 'illuminati-map',
        rate_limit = rate_limit,
        rate_limit_wait = datetime.timedelta(seconds=rate_limit_wait),
        cat_prefix = 'Category:')

    print(f'Getting members of category: {category}...')
    billionaires = wikipedia.categorymembers(category, results=None, subcategories=False)
    # remove non-person list entries
    billionaires = [title for title in billionaires if 'List of ' not in title]
    print('Done!')

    print('Getting page views...')
    views = get_views(wikipedia, billionaires, progress_bar=True)
    views = helpers.sort_dict(views, num_pages)
    print('Done!')

    titles = list(views.keys())
    print('Getting page links...')
    linkshere = get_linkshere(wikipedia, titles, progress_bar=True)
    print('Done!')
    common_links_dict = common_links(titles, linkshere)
    
    full_dict = {billionaire: {
                        'views': views[billionaire],
                        'links': common_links_dict[billionaire]
                        } for billionaire in billionaires}
    
    return full_dict

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
                        help='Width of the generated image in pixels (default: {DEFAULT_CATEGORY})')
    parser.add_argument('--num-pages', type=int, default=None,
                        help='The number of top pages in the category to get data for'
                            '(default: All pages')
    parser.add_argument('--rate-limit', type=bool, default=DEFAULT_RATE_LIMIT,
                        help=f'Use rate limiting to limit calls to Wikipedia '
                            '(default: {DEFAULT_RATE_LIMIT})')
    parser.add_argument('--rate-limit-wait', type=bool, default=DEFAULT_RATE_LIMIT_WAIT,
                        help=f'The amount of time to wait between requests in seconds '
                            '(default: {DEFAULT_RATE_LIMIT_WAIT})')
    return parser

def main(args):
    parser = get_parser(args[0])
    parsed_args = parser.parse_args(args[1:])
    data = get_data(parsed_args.category, parsed_args.num_pages, parsed_args.rate_limit,
                    parsed_args.rate_limit_wait)
    with open(parsed_args.filename, 'wb') as file:
        pickle.dump(data, file)

if __name__ == '__main__':
    main(sys.argv)
