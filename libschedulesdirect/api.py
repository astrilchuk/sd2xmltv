#!/usr/bin/python
# coding=utf-8

import urllib2
import json
import hashlib
import gzip
import StringIO
import logging

class SchedulesDirectApi:

    def __init__(self, username, password):
        self._logger = logging.getLogger(__name__)
        self._username = username
        self._password_hash = hashlib.sha1(password).hexdigest()
        self._base_url = 'https://json.schedulesdirect.org'
        self._base_uri = '/20140530/'
        self._token = None
        self._status = None
        self._lineups = None

    def get_token(self):
        self._logger.debug('get_token()')
        if self._token is not None:
            return self._token
        request = self._get_request('POST', 'token', {'username': self._username, 'password': self._password_hash})
        response = self._get_json_response(request)
        if 'token' in response:
            self._token = response['token']
        return response

    def get_status(self):
        self._logger.debug('get_status()')
        if self._status is not None:
            return self._status
        request = self._get_token_request('GET', 'status')
        response = self._get_json_response(request)
        self._status = response['systemStatus'][0]['status']
        return response

    def is_online(self):
        self._logger.debug('is_online()')
        return self._status == 'Online'

    def _validate_online(self):
        self._logger.debug('_validate_online()')
        if not self.is_online():
            raise Exception('System status is not Online')

    def get_headends_by_postal_code(self, country, postal_code):
        self._logger.debug('get_headends_by_postal_code("%s", "%s")' % (country, postal_code))
        self._validate_online()
        request = self._get_token_request('GET', 'headends?country=%s&postalcode=%s' % (country, postal_code))
        response = self._get_json_response(request)
        return response

    def add_lineup(self, lineup_id):
        self._logger.debug('add_lineup("%s")' % (lineup_id))
        self._validate_online()
        request = self._get_token_request('PUT', 'lineups/' + lineup_id)
        response = self._get_json_response(request)
        return response

    def get_subscribed_lineups(self):
        self._logger.debug('get_lineups()')
        self._validate_online()
        if self._lineups is not None:
            return self._lineups
        request = self._get_token_request('GET', 'lineups')
        response = self._get_json_response(request)
        self._lineups = response["lineups"]
        return self._lineups

    def get_lineup(self, lineup_id):
        self._logger.debug('get_lineup("%s")' % (lineup_id))
        self._validate_online()
        request = self._get_token_request('GET', 'lineups/' + lineup_id)
        response = self._get_json_response(request)
        return response

    def get_schedule_md5s(self, stations):
        """
        Gets schedule md5s in the format:
        {
            "10036": [
                {
                    "days": 13,
                    "md5": "StiEox/4JyAHD4lUvrMCIQ",
                    "modified": "2014-09-18T20:59:07Z"
                }
            ],
            "10091": [
                {
                    "days": 2,
                    "md5": "Ei1DujpwycpFBPXK6fXzjw",
                    "modified": "2014-09-18T20:59:07Z"
                },
                {
                    "days": 4,
                    "md5": "+Yqb0vg+0ZeMm7Jttbapcw",
                    "modified": "2014-09-18T20:59:08Z"
                },
                {
                    "days": 13,
                    "md5": "x9PdBejLYqJmytIHePhWlw",
                    "modified": "2014-09-18T20:59:08Z"
                }
            ]
        }
        :param stations:
        :return:
        """
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('get_schedule_md5s("%s")' % (stations))
        self._validate_online()
        request = self._get_token_request('POST', 'schedules/md5', stations)
        response = self._get_json_response(request)
        return response

    def get_schedules(self, stations):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('get_schedules("%s")' % (stations))
        self._validate_online()
        request = self._get_token_request('POST', 'schedules', stations)
        response = self._get_delimited_json_response(request)
        return response

    def get_programs(self, program_ids):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('get_programs(%s)' % (program_ids))
        self._validate_online()
        request = self._get_token_request('POST', 'programs', program_ids)
        response = self._get_delimited_json_response(request)
        return response

    def _get_request(self, method, uri, post_data = None):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('_get_request("%s", %s)' % (uri, post_data))
        json_data = None
        if post_data is not None:
            json_data = json.dumps(post_data)
        request = urllib2.Request(url = self._base_url + self._base_uri + uri, data = json_data)
        request.get_method = lambda: method
        if json_data is not None:
            request.add_header('Content-Length', len(json_data))
        request.add_header('Content-Type', 'application/json')
        request.add_header('User-Agent', 'sd2xmltv/0.1 (adrian.strilchuk@gmail.com)')
        request.add_header('Accept', 'application/json')
        request.add_header('Accept-Encoding', 'deflate, gzip')
        return request

    def _get_token_request(self, method, uri, data = None):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('_get_token_request("%s", %s)' % (uri, data))
        request = self._get_request(method, uri, data)
        request.add_header('token', self.get_token())
        return request

    def _get_json_response(self, request):
        self._logger.debug('_get_json_response()')
        response = self._get_response(request)
        json_data = json.loads(response)
        #self._logger.debug('response:\n' + json.dumps(json_data, indent = 4))
        return json_data

    def _get_delimited_json_response(self, request, delimiter = '\n'):
        self._logger.debug('_get_delimited_json_response()')
        response = self._get_response(request)
        result = [json.loads(line) for line in response.split(delimiter) if line != '']
        #self._logger.debug('response:\n' + json.dumps(result, indent = 4))
        return result

    def _get_response(self, request):
        self._logger.debug('_get_response()')
        opener = None
        if self._logger.isEnabledFor(logging.DEBUG):
            opener = urllib2.build_opener(urllib2.HTTPSHandler(debuglevel=1))
        else:
            opener = urllib2.build_opener(urllib2.HTTPSHandler())
        response = None
        try:
            response = opener.open(request)
        except urllib2.HTTPError, error:
            self._logger.error(error.read())
        raw_data = response.read()
        if response.headers.get('content-encoding', '') == 'gzip':
            raw_data = StringIO.StringIO(raw_data)
            gzipFile = gzip.GzipFile(fileobj = raw_data)
            raw_data = gzipFile.read()
        #self._logger.debug('raw response:\n' + raw_data)
        return raw_data
