from functools import reduce
import re

from util import gets_raw_data

replace_list = {
    '<std::char_traits<char>>': '',
    '&std::': 'std::',
    '<char,std::char_traits<char>>': '',
    '<char,std::char_traits<char>,std::allocator<char>>': '',
    '::ostream': '',
    '(__fastcall **)': '',
    '(__int64)': '',
    '*(_QWORD *)': '',
    '*(void )': '',
    '(*(unsigned int (__int64, __int64))': '',
    '*(__int64 (_QWORD *, void *))': '',
    # 'std::endl': '"\\n"',
    '(*(__int64 (__int64, const char **))': '',
    '**(void (__fastcall ***)(__int64, char *))':'',
    '(unsigned int)': '',
    '(_QWORD *)': '',
    '((':'(',
    '))':')',
}

replace_capture_regexes = [
    '(\d+)LL',
    '(\d+u)LL', 
    '(\d+)u'
]

# def unpacker(func):
#     return lambda data, arg: func(data, *arg)

@gets_raw_data
def replacer(data):
    """
    Replace old for new for each old,new pair in the param
    """
    for old, new in replace_list.items():
        data = data.replace(old, new)
    return data
    # return reduce(unpacker(str.replace), old_to_new.items(), data)

def delete_suffixes(lines):
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