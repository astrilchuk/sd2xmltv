#!/usr/bin/python
# coding=utf-8

from api import SchedulesDirectApi
from cache import SchedulesDirectCache
from common import Status, Token, Lineup, Program, Schedule, Headend
import logging

class SchedulesDirect(object):

    def __init__(self, username, password, cache_path = './cache/sdcache.db'):
        self._logger = logging.getLogger(__name__)
        self._username = username
        self._password = password
        self._api = SchedulesDirectApi(self._username, self._password)
        self._cache = SchedulesDirectCache(cache_path)
        self._cache.init_database()
        self._force_lineup_refresh = False
        self._force_schedule_refresh = False
        self._force_program_refresh = False

    def get_token(self):
        self._api.get_token()

    def get_status(self):
        return self._api.get_status()

    def is_online(self):
        return self._api.is_online()

    def get_headend_by_postal_code(self, country, postal_code):
        """

        :param country:
        :param postal_code:
        :return:
        :rtype: list of [Headend]
        """
        headends = []
        headends_dict = self._api.get_headends_by_postal_code(country, postal_code)
        for (key, item) in headends_dict.items():
            headends.append(Headend.decode(key, item))

        return headends

    def get_lineups(self, status_lineups):
        """

        :param status_lineups:
        :return:
        :rtype: list of [Lineup]
        """
        lineups = []

        if self._force_lineup_refresh:
            self._logger.info('WARNING: Force refreshing lineups.')

        for (id, modified) in status_lineups:
            lineup = None
            if not self._force_lineup_refresh:
                lineup = self._cache.get_lineup(id, modified.strftime('%Y-%m-%dT%H:%M:%SZ'))
            if lineup is None:
                lineup = self._api.get_lineup(id)
                self._cache.add_lineup(id, lineup['metadata']['modified'], lineup)
            lineups.append(Lineup.decode(lineup))

        return lineups

    def cache_programs(self, programs):
        """

        :param programs:
        :type programs: list of [(str, str)]
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

        self._logger.debug('Found %s program(s) missing from cache.' % (len(program_ids)))

        if len(program_ids) == 0:
            return

        for batch in enumerate_batch(program_ids, 5000):
            self._logger.info('Requesting %s programs from SchedulesDirect.' % (len(batch)))
            programs = self._api.get_programs(batch)
            for program in programs:
                self._cache.add_program(program)
            self._logger.info('Added %s program(s) to program cache.' % (len(programs)))

    def get_program(self, program_id, md5=None):
        program = self._cache.get_program(program_id, md5)
        if program is None:
            return None
        return Program.decode(program)

    def get_schedules(self, station_ids, days):
        """

        :param station_ids:
        :type station_ids: list of [str]
        :param days:
        :type days: int
        :return:
        :rtype: list of [Schedule]
        """
        self._logger.debug('_get_schedules(%s, %s)' % (station_ids, days))
        schedules = []

        station_days_request = [{'stationID':station, 'days':days} for station in station_ids]
        schedule_md5s = self._api.get_schedule_md5s(station_days_request)

        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(schedule_md5s)

        if self._force_schedule_refresh:
            self._logger.info('WARNING: Force refreshing schedules.')

        if not self._force_schedule_refresh:
            for station_id, value in schedule_md5s.items():
                schedule = self._cache.get_schedule(station_id, days, value[0]['md5'])
                if schedule is not None:
                    schedule = Schedule.decode(schedule)
                    schedules.append(schedule)
                    station_days_request = [station_day for station_day in station_days_request if station_day['stationID'] != schedule.station_id]

        if len(station_days_request) == 0:
            return schedules

        result = self._api.get_schedules(station_days_request)
        for schedule in result:
            self._cache.add_schedule(schedule['stationID'], days, schedule['metadata']['md5'], schedule)
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