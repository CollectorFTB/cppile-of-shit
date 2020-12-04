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



def decompiler():
    ida_dump_filename = sys.argv[1]

    processing_funcs = [replacer, replace_cpp_operators, join_stream_lines, delete_suffixes]
    with handle_ida_dump(ida_dump_filename) as decompilation:
        for func in processing_funcs:
            decompilation << func(decompilation.dump)

def main():
    decompiler()

if __name__ == "__main__":
    main()

