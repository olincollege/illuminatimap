'''
Test that helper functions for illuminatimap are working properly.
'''
import pytest

from helpers import common_links, dict_to_nodes, sort_dict, trim_dict

SORT_DICT_CASES = [
    # Tests to add:
    # Returns the correct number of results
    # That a nested dictionary is correctly sorted

    # Checking that an ordered dictionary is returned as itself
    (dict(
        test1=1,
        test2=2,
        test3=3,
        test4=4,
        test5=5,
        test6=6
    ), dict(
        test1=1,
        test2=2,
        test3=3,
        test4=4,
        test5=5,
        test6=6
    ),
    None,
    None
    ),
    # Checking that a nonordered unique dictionary is sorted correctly
    (dict(
        test1=6,
        test2=5,
        test3=4,
        test4=3,
        test5=2,
        test6=1
    ), dict(
        test6=1,
        test5=2,
        test4=3,
        test3=4,
        test2=5,
        test1=6
    ),
    None,
    None
    ),
    # Checking that if numbers are the same, the returned order is the same as
    # the input order
    (dict(
        test1=1,
        test2=1,
        test3=1,
        test4=1,
        test5=1,
        test6=1
    ), dict(
        test1=1,
        test2=1,
        test3=1,
        test4=1,
        test5=1,
        test6=1
    ),
    None,
    None
    ),
    # Checking that an empty dict returns an empty dict
    (dict(), dict(), None, None),

    # Checking that the number of results is trimmed correctly
    (dict(
        test1=6,
        test2=5,
        test3=4,
        test4=3,
        test5=2,
        test6=1
    ), dict(
        test1=6,
        test2=5,
        test3=4,
    ),
    None,
    3
    ),

    # Checking that 0 results can be returned
    (dict(
        test1=6,
        test2=5,
        test3=4,
        test4=3,
        test5=2,
        test6=1
    ), dict(),
    None,
    0
    ),

    # Checking the full list length can be returned
    (dict(
        test1=6,
        test2=5,
        test3=4,
        test4=3,
        test5=2,
        test6=1
    ), dict(
        test1=6,
        test2=5,
        test3=4,
        test4=3,
        test5=2,
        test6=1
    ),
    None,
    6
    ),
]

COMMON_LINKS_CASES = [
    # Testing to see if common links are found for a standard input:
    # Input
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
        # Output
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

    # Testing to see what happens when no commmon links are found:
    # Input
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
        # Output
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

    # Testing a one way link
    # Input
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
        # Output
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

TRIM_DICT_CASES = [
    #Testing the a standard cutoff point
    #Input
    ({'Mark Sommerville': {
        'linkshere': ['Jeff Dusek'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 1,
        'total_views': 15,
        'linkshere_within_category': ['Jeff Dusek']
        },
        'John Geddes': {
        'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 2,
        'total_views': 20,
        'linkshere_within_category': ['Mark Sommerville', 'Jeff Dusek']
        },
        'Jeff Dusek': {
        'linkshere': ['John Geddes', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 3,
        'total_views': 11,
        'linkshere_within_category': ['Mark Sommerville, John Geddes']
        },
    },
    #Cut length
    2,
        # Output
        {'John Geddes': {
        'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 2,
        'total_views': 20,
        'linkshere_within_category': ['Mark Sommerville']
        },
        'Mark Sommerville': {
        'linkshere': ['Jeff Dusek'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 1,
        'total_views': 15,
        'linkshere_within_category': []
        },
    }),
    
    #Testing when the cutoff length is the same as the dictionary length
    #Input
    ({'Mark Sommerville': {
        'linkshere': ['Jeff Dusek'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 1,
        'total_views': 15,
        'linkshere_within_category': ['Jeff Dusek']
        },
        'John Geddes': {
        'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 2,
        'total_views': 20,
        'linkshere_within_category': ['Jeff Dusek','Mark Sommerville']
        },
        'Jeff Dusek': {
        'linkshere': ['John Geddes', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 3,
        'total_views': 11,
        'linkshere_within_category': ['John Geddes','Mark Sommerville']
        },
    },
    #Cut length
    3,
        # Output
        {'John Geddes': {
        'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 2,
        'total_views': 20,
        'linkshere_within_category': ['Jeff Dusek','Mark Sommerville']
        },
        'Mark Sommerville': {
        'linkshere': ['Jeff Dusek'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 1,
        'total_views': 15,
        'linkshere_within_category': ['Jeff Dusek']
        },
        'Jeff Dusek': {
        'linkshere': ['John Geddes', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 3,
        'total_views': 11,
        'linkshere_within_category': ['John Geddes','Mark Sommerville']
        },
    }),

    #Testing a trim length of 0
    #Input
    ({'Mark Sommerville': {
        'linkshere': ['Jeff Dusek'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 1,
        'total_views': 15,
        'linkshere_within_category': ['Jeff Dusek']
        },
        'John Geddes': {
        'linkshere': ['Jeff Dusek', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 2,
        'total_views': 20,
        'linkshere_within_category': ['Jeff Dusek','Mark Sommerville']
        },
        'Jeff Dusek': {
        'linkshere': ['John Geddes', 'Mark Sommerville'],
        'pageviews': {'2021-02-06': 849, '2021-02-07': 904},
        'pageid': 3,
        'total_views': 11,
        'linkshere_within_category': ['John Geddes','Mark Sommerville']
        },
    },
    #Cut length
    0,
        # Output
        {}),
]

DICT_TO_NODES_CASES = [
    # Checking only 1:1 targets
    # Input
    ({'John Smith': {'total_views': 10, 'linkshere_within_category': ['Jane Doe']},
      'Jane Doe': {'total_views': 7, 'linkshere_within_category': ['John Smith']}},
     # Output
     {'nodes': [{'name': 'John Smith', 'group': 10},
                {'name': 'Jane Doe', 'group': 7}, ],
      'links': [{'source': 0, 'target': 1, 'value': 10},
                {'source': 1, 'target': 0, 'value': 7}]}),

    # Checking multiple targets
    # Input
    ({'John Smith': {'total_views': 10, 'linkshere_within_category': ['Jane Doe', 'Bob']},
      'Jane Doe': {'total_views': 7, 'linkshere_within_category': ['John Smith']},
      'Bob': {'total_views': 8, 'linkshere_within_category': ['Jane Doe']}},
     # Output
     {'nodes': [{'name': 'John Smith', 'group': 10},
                {'name': 'Jane Doe', 'group': 7},
                {'name': 'Bob', 'group': 8},],
      'links': [{'source': 0, 'target': 1, 'value': 10},
                {'source': 0, 'target': 2, 'value': 10},
                {'source': 1, 'target': 0, 'value': 7},
                {'source': 2, 'target': 1, 'value': 8}]}),

    # Checking what happens with empty targets
    # Input
    ({'John Smith': {'total_views': 10, 'linkshere_within_category': ['Jane Doe', 'Bob']},
      'Jane Doe': {'total_views': 7, 'linkshere_within_category': ['John Smith']},
      'Bob': {'total_views': 8, 'linkshere_within_category': ['Jane Doe']},
      'Jack': {'total_views': 3, 'linkshere_within_category': []}
      },
     # Output
     {'nodes': [{'name': 'John Smith', 'group': 10},
                {'name': 'Jane Doe', 'group': 7},
                {'name': 'Bob', 'group': 8},
                {'name': 'Jack', 'group': 3}
                ],
      'links': [{'source': 0, 'target': 1, 'value': 10},
                {'source': 0, 'target': 2, 'value': 10},
                {'source': 1, 'target': 0, 'value': 7},
                {'source': 2, 'target': 1, 'value': 8}]}),

    # Testing mutual targets
    #Input
    ({'John Smith': {'total_views': 10, 'linkshere_within_category': ['Jane Doe', 'Bob']},
      'Jane Doe': {'total_views': 7, 'linkshere_within_category': ['John Smith', 'Bob']},
      'Bob': {'total_views': 8, 'linkshere_within_category': ['Jane Doe']}
      },
     # Output
     {'nodes': [{'name': 'John Smith', 'group': 10},
                {'name': 'Jane Doe', 'group': 7},
                {'name': 'Bob', 'group': 8}
                ],
      'links': [{'source': 0, 'target': 1, 'value': 10},
                {'source': 0, 'target': 2, 'value': 10},
                {'source': 1, 'target': 0, 'value': 7},
                {'source': 1, 'target': 2, 'value': 7},
                {'source': 2, 'target': 1, 'value': 8},
                ]})
]

@pytest.mark.parametrize('raw_dict,formatted_dict,nested_sort_key,num_results', SORT_DICT_CASES)
def test_sort_dict(raw_dict, formatted_dict,nested_sort_key,num_results):
    '''
    Check that the function sort_dict works properly.

    Args:
        raw_dict:
        formatted_dict:
    '''
    assert sort_dict(raw_dict,nested_sort_key,num_results) == formatted_dict


@pytest.mark.parametrize('raw_dict,formatted_dict', COMMON_LINKS_CASES)
def test_common_links(raw_dict, formatted_dict):
    '''
    Check that the function common_links works properly.

    Args:
        raw_dict:
        formatted_dict:
    '''
    assert common_links(raw_dict) == formatted_dict


@pytest.mark.parametrize('raw_dict,length,formatted_dict', TRIM_DICT_CASES)
def test_trim_dict(raw_dict, length, formatted_dict):
    '''
    Check that the function trim_dict works properly.

    Args:
        raw_dict:
        formatted_dict:
    '''
    assert trim_dict(raw_dict, length) == formatted_dict


@pytest.mark.parametrize('raw_dict,formatted_dict', DICT_TO_NODES_CASES)
def test_dict_to_nodes(raw_dict, formatted_dict):
    '''
    Check that the function dict_to_nodes works properly.

    Args:
        raw_dict:
        formatted_dict:
    '''
    assert dict_to_nodes(raw_dict) == formatted_dict
