import collections.abc

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # make a dict out of the list
            list_dict = {}
            for idx, item in enumerate(v):
                list_dict[str(idx)] = item

            items.extend(flatten_dict(list_dict, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)