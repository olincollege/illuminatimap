'''
Helper functions for the Illuminati Map project, our SoftDes Spring 2021 midterm.

Authors: Jacob Smilg and Markus Leschly
'''

import time


def get_views(wiki, cat_members):
    search_params = {
        'prop': 'pageviews',
        'pvipdays': 60,
        'format': 'json',
    }

    raw_res = dict()

    for i in range(len(cat_members)//50):
        request_titles = '|'.join(cat_members[50*i:50*(i+1)])
        finished = False
        while not finished:
            search_params['titles'] = request_titles
            result =  wiki.wiki_request(search_params)
            if raw_res.get('query', False):
                raw_res['query']['pages'].update(result['query']['pages'])
            else:
                raw_res.update(result)

            if result.get('continue', False):
                search_params['pvipcontinue'] = result['continue']['pvipcontinue']
                search_params['continue'] = result['continue']['continue']
            else:
                finished = True
        search_params['pvipcontinue'] = ''
        search_params['continue'] = ''
    pages = list(raw_res['query']['pages'].values())
    views = dict()

    for page in pages:
        indiv_views = list(page['pageviews'].values())
        indiv_views = [i for i in indiv_views if i is not None]
        views[page['title']] = sum(indiv_views)

    return views

def get_linkshere(wiki, cat_members):
    search_params = {
        'prop': 'linkshere',
        'lhnamespace': 0,
        'lhlimit': 500,
        'format': 'json',
    }

    raw_res = dict()
    for member in cat_members:
        finished = False
        while not finished:
            search_params['titles'] = member
            result = wiki.wiki_request(search_params)
            if not list(result['query']['pages'].values())[0].get('linkshere', False):
                print(f'linkshere not found for {member}. Trying again in 3 seconds...')
                time.sleep(3.0)
                result = wiki.wiki_request(search_params)
            if raw_res.get('query', False):
                raw_res['query']['pages'].update(result['query']['pages'])
            else:
                raw_res.update(result)

            if result.get('continue', False):
                search_params['lhcontinue'] = result['continue']['lhcontinue']
                search_params['continue'] = result['continue']['continue']
            else:
                finished = True
        search_params['lhcontinue'] = ''
        search_params['continue'] = ''
    pages = list(raw_res['query']['pages'].values())

    linkshere = dict()
    for page in pages:
        print(f'keys for {page["title"]}: {page.keys()}')
        links = page.get('linkshere', False)
        if links:
            linkshere[page['title']] = [linker['title'] for linker in links]
    return linkshere

def common_links(names, links_dict):
    common_links_dict = {name: [] for name in names}
    for name in names:
        for linker in links_dict[name]:
            if linker in names:
                common_links_dict[name].append(linker)
    return common_links_dict

def sort_dict(_dict, num_results=None):
    if num_results is None:
        num_results = len(_dict.keys())

    sorted_dict = dict()
    sorted_keys = sorted(_dict, key=_dict.get, reverse=True)

    for w in sorted_keys[0:num_results]:
        sorted_dict[w] = _dict[w]
    
    return sorted_dict