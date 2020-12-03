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

def delete_suffixes(lines, replace_capture_regexes):
    """
    If line matches regex, replace regex for what was captured from it
    Example:
    sleep(1u); as line
    (\d+)u as regex
    returns sleep(1);

    """
    def yield_replaced_line(line):
        for suffix_regex in replace_capture_regexes:
            if ( match := re.search(suffix_regex, line) ):
                line = line.replace(match.group(), match.group(1)) 
        return line

    return map(yield_replaced_line, lines)