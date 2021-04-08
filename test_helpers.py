'''
Test that helper functions for illuminatimap are working properly.
'''
import pytest
from helpers import (
    sort_dict,
    common_links,
    trim_dict,
    dict_to_nodes,

)

SORT_DICT_CASES = [
    #Tests to add:
    # Returns the correct number of results
        # 0 results
        # random num
        # the full length of the input list
    #That a nested dictionary is correctly sorted

    # Checking that an ordered dictionary is returned as itself
    (dict(
        test1 = 1,
        test2 = 2,
        test3 = 3,
        test4 = 4,
        test5 = 5,
        test6 = 6
         ), dict(
        test1 = 1,
        test2 = 2,
        test3 = 3,
        test4 = 4,
        test5 = 5,
        test6 = 6)),
    # Checking that a nonordered unique dictionary is sorted correctly
    (dict(
        test1 = 6,
        test2 = 5,
        test3 = 4,
        test4 = 3,
        test5 = 2,
        test6 = 1
         ), dict(
        test6 = 1,
        test5 = 2,
        test4 = 3,
        test3 = 4,
        test2 = 5,
        test1 = 6)),
    # Checking that if numbers are the same, the returned order is the same as 
    # the input order
    (dict(
        test1 = 1,
        test2 = 1,
        test3 = 1,
        test4 = 1,
        test5 = 1,
        test6 = 1
         ), dict(
        test1 = 1,
        test2 = 1,
        test3 = 1,
        test4 = 1,
        test5 = 1,
        test6 = 1)),
    # Checking that an empty dict returns an empty dict
    (dict(),dict()),
]

COMMON_LINKS_CASES = [
    #Testing to see if common links are found for a standard input:
    #Input
    ({'Mark Sommerville': {
                'linkshere': ['John Geddes'],
                'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
                'pageid': 1,
                'total_views': 3
            }, 
    'John Geddes': {
            'linkshere': ['Mark Sommerville'],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
            'pageid': 2,
            'total_views': 3
            },    
    },
    #Output
    {'Mark Sommerville': {
                'linkshere': ['John Geddes'],
                'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
                'pageid': 1,
                'total_views': 3,
                'linkshere_within_category': ['John Geddes']
            }, 
    'John Geddes': {
            'linkshere': ['Mark Sommerville'],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
            'pageid': 2,
            'total_views': 3,
            'linkshere_within_category': ['Mark Sommerville']
            },    
    }),

    #Testing to see what happens when no commmon links are found:
    #Input
    ({'Mark Sommerville': {
                'linkshere': ['Jeff Dusek'],
                'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
                'pageid': 1,
                'total_views': 3
            }, 
    'John Geddes': {
            'linkshere': ['Jeff Dusek'],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
            'pageid': 2,
            'total_views': 3
            },    
    },
    #Output
    {'Mark Sommerville': {
                'linkshere': ['Jeff Dusek'],
                'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
                'pageid': 1,
                'total_views': 3,
                'linkshere_within_category': []
            }, 
    'John Geddes': {
            'linkshere': ['Jeff Dusek'],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
            'pageid': 2,
            'total_views': 3,
            'linkshere_within_category': []
            },    
    }),

    #Testing a one way link
    #Input
    ({'Mark Sommerville': {
                'linkshere': ['Jeff Dusek'],
                'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
                'pageid': 1,
                'total_views': 3
            }, 
    'John Geddes': {
            'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
            'pageid': 2,
            'total_views': 3
            },    
    },
    #Output
    {'Mark Sommerville': {
                'linkshere': ['Jeff Dusek'],
                'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
                'pageid': 1,
                'total_views': 3,
                'linkshere_within_category': []
            }, 
    'John Geddes': {
            'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
            'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
            'pageid': 2,
            'total_views': 3,
            'linkshere_within_category': ['Mark Sommerville']
            },    
    }),
]

# TRIM_DICT_CASES = [
#     (inp, out),
# ]

DICT_TO_NODES_CASES = [
    #Checking only 1:1 targets
    #Input
    ({'John Smith': {'value': 10, 'target':['Jane Doe']},
    'Jane Doe': {'value': 7, 'target':['John Smith']}},
    #Output
    {'nodes': [{'name': 'John Smith', 'group': 0},
            {'name': 'Jane Doe', 'group': 0},],
    'links': [{'source': 0, 'target': 1, 'value': 10},
            {'source': 1, 'target': 0, 'value': 7}]}),
    
    #Checking multiple targets
    #Input
    ({'John Doe': {'value': 10, 'target':['Jane Doe','Bob']},
    'Jane Doe': {'value': 7, 'target':['John Smith']},
    'Bob': {'value': 8, 'targets':['Jane Doe']}},
    #Output
    {'nodes': [{'name': 'John Smith', 'group': 0},
            {'name': 'Jane Doe', 'group': 0},
            {'name': 'Bob', 'group': 0},],
    'links': [{'source': 0, 'target': 1, 'value': 10},
            {'source': 0, 'target': 2, 'value': 10},
            {'source': 1, 'target': 0, 'value': 7},
            {'source': 2, 'target': 1, 'value': 8}]})
]


@pytest.mark.parametrize('raw_dict,formatted_dict', SORT_DICT_CASES)
def test_sort_dict(raw_dict, formatted_dict):
    '''
    Check that the function sort_dict works properly.

    Args:
        raw_dict: 
        formatted_dict: 
    '''
    assert sort_dict(raw_dict) == formatted_dict

@pytest.mark.parametrize('raw_dict,formatted_dict', COMMON_LINKS_CASES)
def test_common_links(raw_dict, formatted_dict):
    '''
    Check that the function sort_dict works properly.

    Args:
        raw_dict: 
        formatted_dict: 
    '''
    assert common_links(raw_dict) == formatted_dict

@pytest.mark.parametrize('raw_dict,formatted_dict', DICT_TO_NODES_CASES)
def test_dict_to_nodes(raw_dict, formatted_dict):
    '''
    Check that the function sort_dict works properly.

    Args:
        raw_dict: 
        formatted_dict: 
    '''
    assert dict_to_nodes(raw_dict) == formatted_dict