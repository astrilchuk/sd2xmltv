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
logger.setLevel(logging.WARN)


def get_token(username, password_hash):
    """

    :param username:
    :type username: unicode
    :param password_hash:
    :type password_hash: unicode
    :return:
    """
    logger.debug("get_token()")
    return _post("token", post_data={"username": username, "password": password_hash})


def get_status(token):
    """

    :param token:
    :type token: unicode
    :return:
    """
    logger.debug("get_status()")
    return _get("status", token)


def get_headends_by_postal_code(token, country, postal_code):
    """

    :param token:
    :type token: unicode
    :param country:
    :type country: unicode
    :param postal_code:
    :type postal_code: unicode
    :return:
    """
    logger.debug("get_headends_by_postal_code('%s', '%s')", country, postal_code)
    uri = "headends?country={0}&postalcode={1}".format(country, postal_code)
    return _get(uri, token)


def get_subscribed_lineups(token):
    """

    :param token:
    :type token: unicode
    :return:
    """
    logger.debug("get_lineups()")
    response = _get("lineups", token)
    if "response" in response and response["response"] == "NO_LINEUPS":
        return []
    lineups = response["lineups"]
    return lineups


def add_lineup(token, lineup_id):
    """

    :param token:
    :type token: unicode
    :param lineup_id:
    :type lineup_id: unicode
    :return:
    """
    logger.debug("add_lineup('%s')", lineup_id)
    uri = "lineups/{0}".format(lineup_id)
    return _put(uri, token)


def remove_lineup(token, lineup_id):
    """

    :param token:
    :type token: unicode
    :param lineup_id:
    :type lineup_id: unicode
    :return:
    """
    logger.debug("remove_lineup('%s')", lineup_id)
    uri = "lineups/{0}".format(lineup_id)
    return _delete(uri, token)


def get_lineup(token, lineup_id):
    """

    :param token:
    :type token: unicode
    :param lineup_id:
    :type lineup_id: unicode
    :return:
    """
    logger.debug("get_lineup('%s')", lineup_id)
    uri = "lineups/{0}".format(lineup_id)
    return _get(uri, token)


def get_schedule_md5s(token, stations):
    """

    :param token:
    :type token: unicode
    :param stations:
    :type stations: list[dict]
    :return:
    """
    logger.debug("get_schedule_md5s(%s)", stations)
    return _post("schedules/md5", token, stations)


def get_schedules(token, stations):
    """

    :param token:
    :type token: unicode
    :param stations:
    :type stations: list[dict]
    :return:
    """
    logger.debug("get_schedules(%s)", stations)
    return _post("schedules", token, stations)


def get_programs(token, program_ids):
    """

    :param token:
    :type token: unicode
    :param program_ids:
    :type program_ids: list[unicode]
    :return:
    """
    logger.debug("get_programs(%s)", program_ids)
    return _post("programs", token, program_ids)


def get_metadata(program_ids):
    logger.debug("get_metadata(%s)", program_ids)
    return _post("metadata/programs", post_data=program_ids)


def _get(uri, token=None):
    request = _get_request("GET", uri, token)
    response = _get_response(request)
    return response


def _post(uri, token=None, post_data=None):
    request = _get_request("POST", uri, token, post_data)
    response = _get_response(request)
    return response


def _put(uri, token=None, post_data=None):
    request = _get_request("PUT", uri, token, post_data)
    response = _get_response(request)
    return response


def _delete(uri, token=None, post_data=None):
    request = _get_request("DELETE", uri, token, post_data)
    response = _get_response(request)
    return response


def _get_request(method, uri, token=None, post_data=None):
    """

    :param method:
    :type method: str
    :param uri:
    :type uri: str
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
    request.add_header("User-Agent", "sd2xmltv/0.2 (adrian.strilchuk@gmail.com)")
    request.add_header("Accept", "application/json")
    request.add_header("Accept-Encoding", "deflate, gzip")
    if token is not None:
        request.add_header("token", token)
    return request


def _get_token_request(token, method, uri, data=None):
    """

    :param token:
    :type token: unicode
    :param method:
    :type method: str
    :param uri:
    :type uri: str
    :param data:
    :return:
    """
    logger.debug("_get_token_request('%s', '%s', %s)", method, uri, data)
    request = _get_request(method, uri, data)
    request.add_header("token", token)
    return request


def _get_response(request):
    logger.debug("_get_response()")

    if logger.isEnabledFor(logging.DEBUG):
        opener = urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=1))
    else:
        opener = urllib2.build_opener(urllib2.HTTPSHandler())

    try:
        response = opener.open(request)
    except urllib2.HTTPError, error:
        error = error.read()
        logging.error(error)
        return error

    content_encoding = response.headers.get("content-encoding", "")
    content_type = response.headers.get("content-type")
    encoding = content_type.split("charset=")[-1]

    buf = StringIO.StringIO(response.read())

    if content_encoding == "gzip":
        buf = gzip.GzipFile(fileobj=buf)

    if content_type.startswith("application/json"):
        return json.load(fp=buf, encoding=encoding)

    return unicode(buf.read(), encoding)
