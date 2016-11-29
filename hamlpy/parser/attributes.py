from __future__ import print_function, unicode_literals

import regex

from collections import OrderedDict

from .generic import consume_whitespace, read_symbol, read_number, read_quoted_string, STRING_LITERALS, ParseException

ATTRIBUTE_KEY_REGEX = regex.compile(r'[a-zA-Z0-9-_]+')

re_whitespace = regex.compile(r'([ \t]+)')
re_leading_spaces = regex.compile(r'^\s+', regex.MULTILINE)
re_line = regex.compile(r'.*')


def read_attribute_key(stream):
    """
    Reads an attribute key
    """
    start = stream.ptr

    while True:
        ch = stream.text[stream.ptr]
        if not (('A' <= ch <= 'Z') or ('a' <= ch <= 'z') or ('0' <= ch <= '9') or ch in ('_', '-')):
            break

        stream.ptr += 1

    return stream.text[start:stream.ptr]


def read_attribute_value(stream):
    """
    Reads an attribute's value which may be a string, a number or None
    """
    ch = stream.text[stream.ptr]

    if ch in STRING_LITERALS:
        return read_quoted_string(stream)
    elif ch.isdigit():
        return read_number(stream)
    else:
        read_symbol(stream, ('None', 'none'))
        return None


def read_attribute_value_list(stream):
    """
    Reads an attribute value which is a list of other values
    """
    open_literal = stream.text[stream.ptr]

    assert open_literal in ('(', '[')

    read_tuple = open_literal == '('
    close_literal = ')' if read_tuple else ']'

    data = []

    stream.ptr += 1  # consume opening symbol

    while True:
        consume_whitespace(stream)

        if stream.text[stream.ptr] == close_literal:
            break

        data.append(read_attribute_value(stream))

        consume_whitespace(stream)

        if stream.text[stream.ptr] != close_literal:
            read_symbol(stream, (',',))

    stream.ptr += 1  # consume closing symbol

    return tuple(data) if read_tuple else data


def read_attribute_value_haml(stream):
    """
    Reads an attribute value which is a block of indented HAML
    """
    def whitespace_length():
        r = re_whitespace.match(stream.text, pos=stream.ptr)
        return len(r.group(0))

    initial_indentation = whitespace_length()
    lines = []

    while whitespace_length() >= initial_indentation:
        line = re_line.match(stream.text, pos=stream.ptr).group(0)
        lines.append(line)
        stream.ptr += len(line) + 1

    stream.ptr -= 1  # un-consume final newline which will act as separator between this and next entry

    from ..hamlpy import Compiler
    html = Compiler().process_lines(lines)
    return regex.sub(re_leading_spaces, ' ', html).replace('\n', '').strip()


def read_attribute(stream, assignment_symbols, entry_separator, terminator):
    """
    Reads a single dictionary entry, e.g. :foo => "bar" or foo="bar"
    """
    if stream.text[stream.ptr] in STRING_LITERALS:
        key = read_quoted_string(stream)
    else:
        # attribute keys may be prefixed with : which we ignore
        if stream.text[stream.ptr] == ':':
            stream.ptr += 1

        key = read_attribute_key(stream)

    if not key:
        raise ParseException("Empty attribute key", stream)

    consume_whitespace(stream)

    if stream.text[stream.ptr] in (entry_separator, terminator):
        value = None
    else:
        read_symbol(stream, assignment_symbols)

        consume_whitespace(stream)

        if stream.text[stream.ptr] == '\n':
            stream.ptr += 1

            value = read_attribute_value_haml(stream)
        elif stream.text[stream.ptr] in ('(', '['):
            value = read_attribute_value_list(stream)
        else:
            value = read_attribute_value(stream)

    return key, value


def read_attribute_dict(stream):
    """
    Reads an attribute dictionary, e.g. {:foo => "bar", a => 3} or (foo="bar" a=3)
    """
    data = OrderedDict()

    start, terminator = stream.text[0], stream.text[-1]

    assert start in ('{', '(') and terminator in ('}', ')')

    if start == '{':
        assignment_symbols = ('=>', ':')
        entry_separator = ','
    else:
        assignment_symbols = ('=',)
        entry_separator = None

    stream.ptr += 1

    while True:
        consume_whitespace(stream, include_newlines=True)

        if stream.text[stream.ptr] == terminator:
            break

        key, value = read_attribute(stream, assignment_symbols, entry_separator, terminator)

        data[key] = value

        consume_whitespace(stream)

        if entry_separator and stream.text[stream.ptr] not in (terminator, '\n'):
            read_symbol(stream, (entry_separator,))

    return data
