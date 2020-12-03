'''
TODO:
remove uneeded local variables
replace variables with only 1 usecase
name variables
array size calculation
remove self from class funcs
canary checker
'''

import sys

from replacer import replacer, delete_suffixes
from stream_parser import replace_cpp_operators, join_stream_lines
from util import handle_ida_dump

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
regex_patterns = {
    '\d+LL': 2,
    '\d+uLL': 3, 
    '\d+u': 1
}


def decompiler():
    ida_dump_filename = sys.argv[1]

    with handle_ida_dump(ida_dump_filename) as decompilation:
        decompilation << replacer(decompilation.dump, replace_list)
        decompilation << replace_cpp_operators(decompilation.dump)
        decompilation << join_stream_lines(decompilation.dump)
        decompilation << delete_suffixes(decompilation.dump, regex_patterns)

def main():
    decompiler()

if __name__ == "__main__":
    main()

