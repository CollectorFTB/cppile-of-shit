from functools import reduce
import re

from util import gets_raw_data



def unpacker(func):
    return lambda data, arg: func(data, *arg)

@gets_raw_data
def replacer(data, old_to_new: dict):
    """
    Replace old for new for each old,new pair in the param
    """
    return reduce(unpacker(str.replace), old_to_new.items(), data)

def delete_suffixes(data, suffix_regex_to_len):
    def yield_cut_ending(line):
        for suffix_regex, suffix_len in suffix_regex_to_len.items():
            if ( match := re.search(suffix_regex, line) ):
                return line.replace(( result := match.group() ), result[:-suffix_len]) 
            return line

    return map(yield_cut_ending, data)