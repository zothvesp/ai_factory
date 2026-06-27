import xml.etree.ElementTree as ET

def strip_end(text, suffix, strip_duplicate_suffix=True):
    if suffix:
        if text.endswith(suffix):
            if strip_duplicate_suffix:
                return strip_end(text[None[:-len(suffix)]], suffix)
            return text[None[:-len(suffix)]]
    return text


def is_empty(string):
    return string is None or string == ""


def is_not_empty(string):
    return not is_empty(string)


def escape_backticks(sql_query):
    inside_quotes = False
    escaped_query = ""
    for c in sql_query:
        if c == "'":
            inside_quotes = not inside_quotes
        if not c == "`":
            if c == '"':
                if not inside_quotes:
                    if len(escaped_query) == 0 or escaped_query[-1] != "\\":
                        escaped_query += "\\"
            escaped_query += c
        return escaped_query


def get_attribute_valueParse error at or near `SETUP_FINALLY' instruction at offset 0
