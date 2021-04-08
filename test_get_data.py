'''
Test that formatting the raw data is working properly.
'''
import pytest
from get_data import format_data

FORMAT_DATA_CASES = [
    (inp, out),
]


@pytest.mark.parametrize('raw_dict,formatted_dict', FORMAT_DATA_CASES)
def test_format_data(raw_dict, formatted_dict):
    '''
    Check that the function format_data works properly.

    Args:
        raw_dict: A dictionary representing raw output from the wikipedia API.
        formatted_dict: 
    '''
    assert format_data(raw_dict) == formatted_dict
