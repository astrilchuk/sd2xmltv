#!/usr/bin/python
# coding=utf-8

import urllib2
import json
import gzip
import logging
from . import jsonify
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

_base_url = "https://json.schedulesdirect.org"
_base_uri = "/20141201/"

logger = logging.getLogger(__name__)

def get_token(username, password_hash):  # type: (unicode, unicode) -> Any
    """

    :param username:
    :param password_hash:
    :return:
    """
    logger.debug("get_token()")
    return _post("token", post_data={"username": username, "password": password_hash})


def get_status(token):  # type: (unicode) -> Any
    """

    :param token:
    :return:
    """
    logger.debug("get_status()")
    return _get("status", token)


def get_available_services():  # type: () -> Any
    """

    :return:
    """
    logger.debug("get_available_services()")
    return _get("available")


def get_service_countries():  # type: () -> Any
    """

    :return:
    """
    logger.debug("get_service_countries")
    return _get("available/countries")


def get_headends_by_postal_code(token, country, postal_code):  # type: (unicode, unicode, unicode) -> Any
    """

    :param token:
    :param country:
    :param postal_code:
    :return:
    """
    logger.debug("get_headends_by_postal_code('%s', '%s')", country, postal_code)
    uri = "headends?country={0}&postalcode={1}".format(country, postal_code)
    return _get(uri, token)


def get_subscribed_lineups(token):  # type: (unicode) -> Any
    """

    :param token:
    :return:
    """
    logger.debug("get_lineups()")
    return _get("lineups", token)


def add_lineup(token, lineup_id):  # type: (unicode, unicode) -> Any
    """

    :param token:
    :param lineup_id:
    :return:
    """
    logger.debug("add_lineup('%s')", lineup_id)
    uri = "lineups/{0}".format(lineup_id)
    return _put(uri, token)


def remove_lineup(token, lineup_id):  # type: (unicode, unicode) -> Any
    """

    :param token:
    :param lineup_id:
    :return:
    """
    logger.debug("remove_lineup('%s')", lineup_id)
    uri = "lineups/{0}".format(lineup_id)
    return _delete(uri, token)


def get_lineup(token, lineup_id):  # type: (unicode, unicode) -> Any
    """

    :param token:
    :param lineup_id:
    :return:
    """
    logger.debug("get_lineup('%s')", lineup_id)
    uri = "lineups/{0}".format(lineup_id)
    return _get(uri, token)


def get_schedule_md5s(token, stations):  # type: (unicode, List[dict]) -> Any
    """

    :param token:
    :param stations:
    :return:
    """
    logger.debug("get_schedule_md5s(%s)", stations)
    return _post("schedules/md5", token, stations)


def get_schedules(token, stations):  # type: (unicode, List[dict]) -> Any
    """

    :param token:
    :param stations:
    :return:
    """
    logger.debug("get_schedules(%s)", stations)
    return _post("schedules", token, stations)


def get_programs(token, program_ids):  # type: (unicode, List[unicode]) -> Any
    """

    :param token:
    :param program_ids:
    :return:
    """
    logger.debug("get_programs(%s)", program_ids)
    return _post("programs", token, program_ids)


def get_metadata(program_ids):  # type: (List[unicode]) -> Any
    logger.debug("get_metadata(%s)", program_ids)
    return _post("metadata/programs", post_data=program_ids)


def _get(uri, token=None):  # type: (unicode, Optional[unicode]) -> Any
    request = _get_request(u"GET", uri, token)
    response = _get_response(request)
    return response


def _post(uri, token=None, post_data=None):  # type: (unicode, Optional[unicode], Any) -> Any
    request = _get_request(u"POST", uri, token, post_data)
    response = _get_response(request)
    return response


def _put(uri, token=None, post_data=None):  # type: (unicode, Optional[unicode], Any) -> Any
    request = _get_request(u"PUT", uri, token, post_data)
    response = _get_response(request)
    return response


def _delete(uri, token=None, post_data=None):  # type: (unicode, Optional[unicode], Any) -> Any
    request = _get_request(u"DELETE", uri, token, post_data)
    response = _get_response(request)
    return response


def _get_request(method, uri, token=None, post_data=None):  # type: (unicode, unicode, Optional[unicode], Any) -> Any
    """

    :param method:
    :param uri:
    :param post_data:
    :return:
    """
    logger.debug("_get_request('%s', '%s', '%s', %s)", method, uri, token, post_data)
    json_data = None
    if post_data is not None:
        json_data = jsonify(post_data)
    request = urllib2.Request(url=_base_url + _base_uri + uri, data=json_data)
    request.get_method = lambda: method
    if json_data is not None:
        request.add_header("Content-Length", len(json_data))
    request.add_header("Content-Type", "application/json; charset=utf-8")
    request.add_header("User-Agent", "sd2xmltv/0.2.1 (adrian.strilchuk@gmail.com)")
    request.add_header("Accept", "application/json")
    request.add_header("Accept-Encoding", "deflate, gzip")
    if token is not None:
        request.add_header("token", token)
    return request


def _get_token_request(token, method, uri, data=None):  # type: (unicode, unicode, unicode, Any) -> Any
    """

    :param token:
    :param method:
    :param uri:
    :param data:
    :return:
    """
    logger.debug("_get_token_request('%s', '%s', %s)", method, uri, data)
    request = _get_request(method, uri, data)
    request.add_header("token", token)
    return request


def _get_response(request):  # type: (Any) -> Any
    logger.debug("_get_response()")

    if logger.isEnabledFor(logging.DEBUG):
        opener = urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=1))
    else:
        opener = urllib2.build_opener(urllib2.HTTPSHandler())

    try:
        response = opener.open(request)
    except urllib2.HTTPError, error_response:
        response = error_response

    content_encoding = response.headers.get("content-encoding", "")
    content_type = response.headers.get("content-type")
    encoding = content_type.split("charset=")[-1]

    buf = StringIO.StringIO(response.read())

    if content_encoding == "gzip":
        buf = gzip.GzipFile(fileobj=buf)

    if content_type.startswith("application/json"):
        return json.load(fp=buf, encoding=encoding)

    return unicode(buf.read(), encoding)
