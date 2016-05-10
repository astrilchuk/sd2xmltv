__author__ = 'Adrian Strilchuk'

from datetime import datetime, date
import json


def jsonify(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(u",", u":"))


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


def batchx(iterable, batch_size):
    for index in xrange(0, len(iterable), batch_size):
        yield iterable[index:index + batch_size]


def batched(iterable, batch_size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) != 0:
        yield batch


def result_iterator(cursor, fetch_size=250):
    results = cursor.fetchmany(fetch_size)
    while results:
        for result in results:
            yield result
        results = cursor.fetchmany(fetch_size)
