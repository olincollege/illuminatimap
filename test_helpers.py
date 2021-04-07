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
    (inp, out),
]

COMMON_LINKS_CASES = [
    (inp, out),
]

TRIM_DICT_CASES = [
    (inp, out),
]

DICT_TO_NODES_CASES = [
    (inp, out),
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
