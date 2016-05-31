from datetime import datetime, date


# http://stackoverflow.com/questions/14163399/convert-list-of-datestrings-to-datetime-very-slow-with-python-strptime
def parse_datetime(dt_str):
    return datetime(*map(int, [dt_str[0:4], dt_str[5:7], dt_str[8:10], dt_str[11:13], dt_str[14:16], dt_str[17:19]]))


def parse_date(d_str):
    return date(*map(int, d_str.split(u"-")))


def unique(iterable, key_func=None):
    if key_func is None:
        key_func = lambda x: x
    seen = set()
    for item in iterable:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            yield item
