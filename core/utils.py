
def merge_dicts(dictionaries):
    result = {}
    for dictionary in dictionaries:
        result.update(dictionary)
    return result
