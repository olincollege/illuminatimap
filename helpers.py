'''
Helper functions for the Illuminati Map project.

Authors: Jacob Smilg and Markus Leschly
'''

def sort_dict(_dict, nested_sort_key=None, num_results=None):
    '''
    Sort a dictionary by its values.

    Parameters:
        _dict (dict): The dictionary to be sorted. Each key's value should be an integer.
        nested_sort_key: Optional, defaults to None. If the dictionary is formatted as a nested
                        dictionary, specify this as the key for which nested value the dictionary
                        should be sorted by.
        num_results (int): Optional, defaults to None. If specified, will return a sorted dictionary
            of length num_results consisting of the keys with the highest values. If left None, returns
            the entire sorted dictionary.
    
    Returns:
        A new dictionary, sorted by its values.
    '''
    if num_results is None:
        num_results = len(_dict.keys())

    sorted_dict = dict()
    if nested_sort_key is None:
        sorted_keys = sorted(_dict, key=_dict.get, reverse=True)
    else:
        sorted_keys = sorted(_dict, key=lambda x: (_dict[x][nested_sort_key]), reverse=True)

    for w in sorted_keys[0:num_results]:
        sorted_dict[w] = _dict[w]
    
    return sorted_dict

def common_links(names, links_dict):
    keep = []
    common_links_dict = {name: [] for name in names}
    for name in names:
        for linker in links_dict[name]:
            if linker in names:
                keep.append(name)
                common_links_dict[name].append(linker)
    
    delete = [name for name in common_links_dict.keys() if name not in keep]

    if len(delete):
        for name in delete:
            del common_links_dict[name]

    return common_links_dict

def trim_dict(_dict, length):
    _dict = sort_dict(_dict, nested_sort_key='views', num_results=length)
    for key in _dict.keys():
        _dict[key]['links'] = list(filter(lambda link: link in _dict.keys(), _dict[key]['links']))
    return _dict

def dict_to_nodes(_dict, target_key='targets', value_key='value'):
    '''
    Convert a dictionary of sources and targets to a dictionary of nodes and edges.

    Input formatted as {'John Doe': {value: 10, targets:['Jane Doe']},
                        'Jane Doe': {value: 7, targets:['John Smith']},
                        'Bob': {value: 8, targets:['Alice']},
                        'Alice': {value: 5, targets:['Bob']}}
    is converted to the format {'nodes': [{'name': 'John Smith', 'group': 0},
                                        {'name': 'Jane Doe', 'group': 0},
                                        {'name': 'Bob', 'group': 0},
                                        {'name': 'Alice', 'group': 0}],
                                'links': [{'source': 0, 'target': 1, 'value': 10},
                                        {'source': 1, 'target': 0, 'value': 7},
                                        {'source': 2, 'target': 3, 'value': 8},
                                        {'source': 3, 'target': 2, 'value': 5}]}
    
    Parameters:
        _dict (dict): A dictionary of sources and targets. See above for example.
        target_key (str): Optional. The key for the target list. Defaults to 'targets'.
        value_key (str): Optional. The key for the source value. Defaults to 'value'.
    '''
    sources = _dict.keys()
    #unfold dict into list of tuples representing connections: (source, target, value)
    datalist = []
    for source in sources:
        for target in _dict[source][target_key]:
            datalist.append((source, target, _dict[source][value_key]))

    data = dict()
    names_with_indexes = {name:index for index, name in enumerate(sources)}
    data['nodes'] = [{'name': source, 'group': _dict[source][value_key]} for source in sources]
    data['links'] = [  {'source': names_with_indexes[source],
                        'target': names_with_indexes[target], 
                        'value': value} for source, target, value in datalist]
    return data