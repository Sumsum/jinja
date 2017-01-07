import math
from .datastructures import List
from markupsafe import escape


def to_number(value):
    """
    Helper function to cast strings to to int or float.
    """
    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError:
            value = float(value)
    return value


def do_abs(value):
    """
    Returns the absolute value, type casts strings to numbers before applying absolute value.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L302
    """
    return abs(to_number(value))


def do_append(a, b):
    """
    Concatenate two strings or objects that has a string representation.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L223
    """
    return '{}{}'.format(a, b)


def do_ceil(value):
    """
    Return the ceiling of value as a number (or a string that can be casted to a
    number), the smallest integer value greater than or equal to value.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L344
    """
    return math.ceil(to_number(value))


def do_divided_by(value, divide_by):
    """
    Ruturn value divided by divide_by, string arguments will be casted to numbers.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L323
    """

    value = to_number(value)
    divide_by = to_number(divide_by)
    if isinstance(value, int) and isinstance(value, int):
        return value // divide_by
    return value / divide_by


def do_modulo(value, modulo):
    """
    Return the value modulo by modulo, string arguments will be casted to numbers.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L329
    """
    return to_number(value) % to_number(modulo)


def do_compact(value, remove=None):
    """
    Removes values from a list.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L190
    """
    return List(v for v in value if v != remove)


def do_map(value, attribute):
    """
    Creates a list of values by extracting the values of a named attribute from another object.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L175
    """
    def proc(obj):
        if isinstance(obj, dict):
            return obj.get(attribute, None)
        if hasattr(obj, 'to_liquid'):
            obj.to_liquid()
        val = getattr(obj, attribute, None)
        if callable(val):
            return val()
        return val

    if isinstance(value, dict):
        return List(proc(value))

    res = List()
    for obj in value:
        v = proc(obj)
        if v is not None:
            res.append(v)
    return res


def do_escape(s):
    """
    Escapes a string by replacing characters with escape sequences (so that the
    string can be used in a URL, for example). It doesn’t change strings that
    don’t have anything to escape.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L35
    """
    if s is None:
        return None
    return escape(s)


def do_escape_once(s):
    """
    Escapes a string without changing existing escaped entities. It doesn’t
    change strings that don’t have anything to escape.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L40
    """
    if s is None:
        return None
    return escape(s
        .replace('&amp;', '&')
        .replace('&gt;', '>')
        .replace('&lt;', '<')
        .replace('&#39;', "'")
        .replace('&#34;', '"')
        .replace('&quot;', '"')
    )


def do_floor(value):
    """
    Rounds a number down to the nearest whole number. We try to convert the
    input to a number before the filter is applied.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L350
    """
    return math.floor(to_number(value))


def do_lstrip(s):
    """
    Removes all whitespaces (tabs, spaces, and newlines) from the beginning of
    a string. The filter does not affect spaces between words.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L96
    """
    return s.lstrip()


def do_rstrip(s):
    """
    Removes all whitespace (tabs, spaces, and newlines) from the right side of
    a string.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L100
    """
    return s.rstrip()


def do_minus(a, b):
    """
    Subtracts a number from another number.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L313
    """
    return to_number(a) - to_number(b)


def do_newline_to_br(s):
    """
    Replaces every newline (\n) with an HTML line break (<br>).
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L240
    """
    return s.replace('\n', '<br />\n')


def do_plus(a, b):
    """
    Adds a number to another number.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L308
    """
    return to_number(a) + to_number(b)


def do_prepend(a, b):
    """
    Adds the specified string to the beginning of another string.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L502
    """
    return '{}{}'.format(b, a)


def do_remove(s, remove):
    """
    Removes every occurrence of the specified substring from a string.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L213
    """
    return s.replace(str(remove), '')


def do_remove_first(s, remove):
    """
    Removes only the first occurrence of the specified substring from a string.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L218
    """
    return s.replace(str(remove), '', 1)


def do_len(value):
    if value is None:
        return 0
    return len(value)


def do_split(s, sep):
    """
    Divides an input string into an array using the argument as a separator.
    split is commonly used to convert comma-separated items from a string to an
    array.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L88
    """
    if s is None:
        return List()
    return List(str(s).split(str(sep)))


def do_strip(s):
    """
    Removes all whitespace (tabs, spaces, and newlines) from both the left and
    right side of a string. It does not affect spaces between words.
    https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/lib/liquid/standardfilters.rb#L92
    """
    return str(s).strip()
