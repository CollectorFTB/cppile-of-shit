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

def delete_suffixes(data, suffix_regexes):
    def yield_cut_ending(line):
        for suffix_regex in suffix_regexes:
            re.search(suffix_regex, line)
            if ( match := re.search(suffix_regex, line) ):
                return line.replace(match.group(), match.group(1)) 
        return line

    return map(yield_cut_ending, data)