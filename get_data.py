'''
Data acquisition code for the Illuminati Map project, our SoftDes Spring 2021 midterm.

Authors: Jacob Smilg and Markus Leschly
'''

import sys
import pickle
import argparse
from datetime import timedelta, datetime
from mediawiki import MediaWiki
from helpers import common_links


DEFAULT_CATEGORY = 'American_billionaires'
DEFAULT_RATE_LIMIT = True
DEFAULT_RATE_LIMIT_WAIT = 1.0   # seconds

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
    '''
    Gets the titles, page ids, views from the last 60 days, and links to the Wikipedia pages in a
    specified category. Stores the acquired data as returned by the API in a list of dictionaries
    to be processed elsewhere.

    For details on the format returned by the API, see the official documentation, and
    be sure it specifies format version 2. This function uses a "generator," for which info can be
    found in the official documentation.

    Parameters:
        wiki: A MediaWiki instance configured to access Wikipedia. It would be smart to rate limit
            it as well, since this function can potentially send a large amount of requests.
        category: A string representing the name of the Wikipedia category for data to be gathered
            from.

    Returns:
        A list of dictionaries containing the responses from Wikipedia. A large amount of this data
        is empty, and should be trimmed and formatted elsewhere.
    '''
    # set up a dictionary of request parameters for the generator.
    search_params = {
        'gcmtitle': f'Category:{category}',
    }

    search_params.update(GENERAL_SEARCH_PARAMS)

    print(f'Getting information for category: {category}...')

    # set up the list to store the API data in
    pages = []

    # used for "continuing" a request; see API documentation for a proper explanation but basically
    # sometimes we get a "continue" key in the API return that lets us get more data starting from
    # where the previous request left off if there was too much to fit in one API return.
    cont = dict()

    # stuff to keep track of progress to be sure nothing got stuck
    start_time = datetime.now()
    last_update = timedelta(seconds=1)
    requests_count = 1

    finished = False
    while not finished:
        # make a copy for safety, makes sure continue stuff doesn't persist, since there are a few
        # different continue parameters that aren't always returned.
        params = search_params.copy()
        params.update(cont)

        # get data from the API and tack what it gives onto the end of our list
        result = wiki.wiki_request(params)
        pages.extend(result['query']['pages'])

        # figure out how much time has passed since the function started, and remove milliseconds
        # from it so it looks nice for printing
        elapsed_time = datetime.now() - start_time
        elapsed_time_str = str(elapsed_time).split('.')[0]

        # continue if we need to
        if result.get('continue', False):
            cont = result['continue']

            # progress message - only display if it's been more than a second so we don't waste
            # time printing to the terminal a bunch
            if elapsed_time - last_update > timedelta(seconds=1):
                print(f'[{elapsed_time_str}]   Sending request #{requests_count}...'.ljust(80),
                    end='\r', flush=True)
                last_update = elapsed_time
                requests_count += 1
        else:
            # no continue returned from API means we're done
            print(f'[{elapsed_time_str}]   Done getting data!'.ljust(80))
            finished = True

    return pages

def format_data(data):
    '''
    Formats a list of raw data from multiple Wikipedia API requests into a usable dictionary.

    Removes any data for "List" pages, which are detected by checking if "List of" is in the page
    title. This approach probably isn't flawless, but it works for the scope of this project.

    Parameters:
        data: A list of dictionaries containing API returns from Wikipedia, as returned by
            get_generator()

    Returns:
        A dictionary constructed from the data input, formatted similar to the following:
        {'Category Member Page Title': {
            'linkshere': ['Page Title 1', 'Page Title 2', ....],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904, ....},
            'pageid': 60977798,
            'total_views': 19849,
            'linkshere_within_category': ['Page Title 2', ....]
        }, ....}

    '''
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
            formatted_data[title]['linkshere'].extend(
                [linkpage['title'] for linkpage in page['linkshere']])
        if page.get('pageviews', False):
            formatted_data[title]['pageviews'].update(page['pageviews'])
    for page in formatted_data:
        page_views = {date: views for date, views in
            formatted_data[page]['pageviews'].items() if views is not None}
        formatted_data[page]['total_views'] = sum(list(page_views.values()))
    print('Finding common links...')
    formatted_data = common_links(formatted_data)
    print('Done formatting data!')
    return formatted_data

def get_data(category, rate_limit, rate_limit_wait=1):
    '''
    Creates an MediaWiki instance for Wikipedia and obtains information about a specified category
    of pages.

    Parameters:
        category: A string representing the title of a Wikipedia category, with spaces replaced by
            underscores, such as 'American_billionaires' or 'Science_communicators'.
        rate_limit: A boolean that should be set to True if rate limiting the MediaWiki instance is
            necessary/desired, and False if not.
        rate_limit_wait: Optional. A number representing the number of seconds to wait between
            requests if rate limiting is enabled. Defaults to 1.
    '''
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
                        help=f'Width of the generated image in pixels '
                             f'(default: {DEFAULT_CATEGORY})')
    parser.add_argument('--rate-limit', type=bool, default=DEFAULT_RATE_LIMIT,
                        help='Use rate limiting to limit calls to Wikipedia '
                            f'(default: {DEFAULT_RATE_LIMIT})')
    parser.add_argument('--rate-limit-wait', type=bool, default=DEFAULT_RATE_LIMIT_WAIT,
                        help='The amount of time to wait between requests in seconds '
                            f'(default: {DEFAULT_RATE_LIMIT_WAIT})')
    return parser

def main(args):
    '''
    Main function for getting data. Calls other functions to get Wikipedia data and pickles the
    results into a specified file.

    Parameters:
        args: A list of command line arguments. Run "python get_data.py -h" in a terminal for
            details.
    '''
    parser = get_parser(args[0])
    parsed_args = parser.parse_args(args[1:])
    data = get_data(parsed_args.category, parsed_args.rate_limit,
                    parsed_args.rate_limit_wait)
    with open(parsed_args.filename, 'wb') as file:
        pickle.dump(data, file)

if __name__ == '__main__':
    main(sys.argv)
