from parse import Parser

STREAM_OPERATORS = ['>>', '<<']


def replace_cpp_operators(lines):
    """
    Turns each line that looks like
    std::operator<<(v1, "something");
    into
    v1 << "something";
    """
    def yield_parse_result(line):
        std_operator_parser = Parser('{indent}std::operator{op}({params});') 
        if (result := std_operator_parser.parse(line)) and result.named['op'] in STREAM_OPERATORS:
            indent, op, params = result.named['indent'], ' ' + result.named['op'], result.named['params']
            return indent + op.join(params.split(',')) + ';'
        else:
            return line
        
    return map(yield_parse_result, lines)

def join_stream_lines(lines):
    """
    Turns two lines that look like
    v1 = std::cout << "something";
    v2 = v1 << "something else";
    into one line that looks like
    v2 = std::cout << "something" << "something else";
    """
    def yield_parse_result(line1, line2):
        subsitution_parser = Parser('{}v{var_name} = {value};')
        if (result := subsitution_parser.parse(line1)) and 'v'+result.named['var_name'] in line2 and any(op in line2 for op in STREAM_OPERATORS):
            var_name, value = result.named['var_name'], result.named['value']
            return '', line2.replace('v'+var_name, value)
        else:
            return line1, line2
    
    lines = list(lines)
    for i, line in enumerate(lines[:-1]):
        lines[i], lines[i+1] = yield_parse_result(lines[i], lines[i+1])

    return filter(lambda x: x, lines)
