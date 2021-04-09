'''
Test that formatting the raw data is working properly.
'''
from get_data import format_data

FORMAT_DATA_CASE = [
    # Check that a standard return from Wikipedia is formatted properly. Wikipedia consistently
    # returns the data in this exact format, so other tests aren't necessary.
    [
        {
            'pageid': 1938,
            'ns': 0,
            'title':'Andrew Carnegie',
            'pageviews': {
                '2021-02-08': 3218,
                '2021-02-09': 9644, #etc etc
            }
        },
        {
            'pageid': 3747,
            'ns': 0,
            'title': 'Bill Gates',
            'linkshere': [
                {
                    'pageid': 663,
                    'ns': 0,
                    'title': 'Apollo 8',
                    'redirect': False
                },
                {
                    'pageid': 675,
                    'ns': 0,
                    'title': 'Affirming the consequent',
                    'redirect': False
                },
            ]
        },
        {
            'pageid': 11857,
            'ns': 0,
            'title': 'George Lucas'
        },
        {
            'pageid': 14059,
            'ns': 0,
            'title': 'Howard Hughes'
        }
    ],
    {
        'Andrew Carnegie':
        {
            'linkshere': [],
            'pageviews':
            {
                '2021-02-08': 3218,
                '2021-02-09': 9644
            },
            'pageid': 1938,
            'total_views': 12862,
            'linkshere_within_category': []
        },
        'Bill Gates':
        {
            'linkshere': ['Apollo 8', 'Affirming the consequent'],
            'pageviews': {},
            'pageid': 3747,
            'total_views': 0,
            'linkshere_within_category': []
        },
        'George Lucas':
        {
            'linkshere': [],
            'pageviews': {},
            'pageid': 11857,
            'total_views': 0,
            'linkshere_within_category': []
        },
        'Howard Hughes':
        {
            'linkshere': [],
            'pageviews': {},
            'pageid': 14059,
            'total_views': 0,
            'linkshere_within_category': []
        }
    }
]


# @pytest.mark.parametrize('raw_dict,formatted_dict', FORMAT_DATA_CASES)
def test_format_data():
    '''
    Check that the function format_data works properly.

    Args:
        raw_dict: A dictionary representing raw output from the wikipedia API.
        formatted_dict: A properly formatted/filtered dataset.
    '''
    assert format_data(FORMAT_DATA_CASE[0]) == FORMAT_DATA_CASE[1]
