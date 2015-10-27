#!/usr/bin/python
# coding=utf-8

from api import SchedulesDirectApi
from cache import SchedulesDirectCache
from common import Status, Token, LineupMapping, Program, Schedule, Headend, Lineup, AddRemoveLineupResponse
import logging

class SchedulesDirect(object):

    def __init__(self, username, password, cache_path = './sdcache.db'):
        self._logger = logging.getLogger(__name__)
        self._api = SchedulesDirectApi(username, password)
        self._cache = SchedulesDirectCache(cache_path)
        self._cache.init_database()
        self._force_lineup_refresh = False
        self._force_program_refresh = False
        self._subscribed_lineups = None

    def get_token(self):
        self._api.get_token()

    def get_status(self):
        return self._api.get_status()

    def is_online(self):
        return self._api.is_online()

    def get_headends_by_postal_code(self, country, postal_code):
        """

        :param country:
        :param postal_code:
        :return:
        :rtype: list[Headend]
        """
        headends = []
        headends_dict = self._api.get_headends_by_postal_code(country, postal_code)
        for headend in headends_dict:
            headends.append(Headend.decode(headend))

        return headends

    def get_subscribed_lineups(self):
        """

        :return:
        :rtype: list[Lineup]
        """
        if self._subscribed_lineups is not None:
            return self._subscribed_lineups
        self._subscribed_lineups = []
        lineups_dict = self._api.get_subscribed_lineups()
        for lineup_dict in lineups_dict:
            self._subscribed_lineups.append(Lineup.decode(lineup_dict))

        return self._subscribed_lineups

    def add_lineup(self, lineup_id):
        response = self._api.add_lineup(lineup_id)
        self._subscribed_lineups = None
        return AddRemoveLineupResponse.decode(response)

    def remove_lineup(self, lineup_id):
        response = self._api.remove_lineup(lineup_id)
        self._subscribed_lineups = None
        return AddRemoveLineupResponse.decode(response)

    def get_lineup_mapping(self, lineup_id, modified=None):
        lineup_mapping = None

        if not self._force_lineup_refresh and modified is not None:
            lineup_mapping = self._cache.get_lineup(lineup_id, modified.strftime('%Y-%m-%dT%H:%M:%SZ'))

        if lineup_mapping is None:
            lineup_mapping = self._api.get_lineup(lineup_id)
            self._cache.add_lineup(lineup_id, lineup_mapping['metadata']['modified'], lineup_mapping)

        return LineupMapping.decode(lineup_mapping)

    def get_lineup_mappings(self, status_lineups):
        """

        :param status_lineups:
        :return:
        :rtype: list[LineupMapping]
        """
        lineup_mappings = []

        if self._force_lineup_refresh:
            self._logger.info('WARNING: Force refreshing lineups.')

        for (lineup_id, modified) in status_lineups:
            lineup_mapping = self.get_lineup_mapping(lineup_id, modified)
            lineup_mappings.append(lineup_mapping)

        return lineup_mappings

    def cache_programs(self, programs):
        """

        :param programs:
        :type programs: list[(str, str)]
        :return:
        """
        self._logger.debug('Searching for uncached programs...')

        program_ids = set()

        if self._force_program_refresh:
            self._logger.info('WARNING: Force refreshing programs.')

        for (program_id, md5) in programs:
            if program_id in program_ids:
                continue
            if self._force_program_refresh or not self._cache.program_exists(program_id, md5):
                program_ids.add(program_id)

        self._logger.info('Found %s program(s) missing from cache.' % (len(program_ids)))

        if len(program_ids) == 0:
            return

        for batch in enumerate_batch(program_ids, 5000):
            self._logger.info('Requesting %s programs from SchedulesDirect.' % (len(batch)))
            programs = self._api.get_programs(batch)
            self._logger.info('Adding program(s) to program cache.')
            self._cache.add_programs(programs)
            self._logger.info('Added %s program(s) to program cache.' % (len(programs)))

    def get_program(self, program_id, md5=None):
        program = self._cache.get_program(program_id, md5)
        if program is None:
            return None
        return Program.decode(program)

    def get_schedules(self, station_ids, dates=None):
        """

        :param station_ids:
        :type station_ids: list[str]
        :return:
        :rtype: list[Schedule]
        """
        self._logger.debug('_get_schedules("%s","%s")' % (station_ids, dates))
        schedules = []

        if dates is None:
            schedules_request = [{'stationID':station} for station in station_ids]
        else:
            schedules_request = [{'stationID':station, 'date':dates} for station in station_ids]

        schedules_response = self._api.get_schedules(schedules_request)

        for schedule in schedules_response:
            schedules.append(Schedule.decode(schedule))

        return schedules

def enumerate_batch(all_items, batch_size):
    batch = []
    for item in all_items:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) != 0:
        yield batch
        batch = []