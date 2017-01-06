import math
from .datastructures import List


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
