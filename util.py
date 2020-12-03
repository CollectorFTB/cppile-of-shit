from contextlib import contextmanager
from dataclasses import dataclass

def as_lines(data):
    return data.splitlines()

def as_data(lines):
    return '\n'.join(lines)

def gets_raw_data(func):
    def wrapper(lines, *args, **kwargs):
        data = as_data(lines)
        retval = func(data, *args, **kwargs)
        return as_lines(retval)
    return wrapper



@dataclass
class IDADump:
    dump: list

    def __lshift__(self, other):
        self.dump = other


@contextmanager
def handle_ida_dump(filename: str) -> IDADump:
    with open(filename, 'r') as ida_dump:
        ida_decompilation = IDADump(as_lines(ida_dump.read()))
    
    yield ida_decompilation

    with open('output.cpp', 'w') as output:
        output.write(as_data(ida_decompilation.dump))