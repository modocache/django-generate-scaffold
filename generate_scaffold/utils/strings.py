import keyword
import re


def dumb_capitalized(s):
    return s[0].upper() + s[1:]


def get_valid_variable(candidate):
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', candidate)
    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)

    if any([keyword.iskeyword(v) for v in [s, s.lower()]]):
        return None

    return s
