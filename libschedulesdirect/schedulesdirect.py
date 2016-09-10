#!/usr/bin/python
# coding=utf-8

import api
from . import batched, parse_datetime, parse_date
from cache import SchedulesDirectCache
from common import Status, LineupMap, LineupMapList, ScheduleList, Headend, Lineup, ChangeLineupResponse, ServiceRegion
import logging
import hashlib


class SchedulesDirect(object):
    def __init__(self, username, password, cache_path="./sdcache.db"):
        self._logger = logging.getLogger(__name__)  # type: logging.Logger

        self._username = username  # type: unicode

        self._password = hashlib.sha1(password).hexdigest()  # type: unicode

        self._cache = SchedulesDirectCache(cache_path)  # type: SchedulesDirectCache

        self._cache.init_database()

        self._force_program_refresh = False  # type: bool

        self._subscribed_lineups = None  # type: List[Lineup]

        self._token = None  # type: unicode

        self._status = None  # type: Status

    def get_token(self):
        self._token = api.get_token(self._username, self._password)["token"]

    def get_status(self):
        self._status = Status.from_dict(api.get_status(self._token))
        return self._status

    def is_online(self):
        return self._status.system_status.status == u"Online"

    def get_service_countries(self):
        """

        :return:
        """
        service_region_dict = api.get_service_countries()

        return [ServiceRegion.from_dict(service_region) for service_region in service_region_dict]

    def get_headends_by_postal_code(self, country, postal_code):
        """

        :param country:
        :param postal_code:
        :return:
        :rtype: list[Headend]
        """
        headends_dict = api.get_headends_by_postal_code(self._token, country, postal_code)

        return [Headend.from_dict(headend) for headend in headends_dict]

    def get_subscribed_lineups(self):  # type: () -> List[Lineup]
        """

        :return:
        """
        if self._subscribed_lineups is not None:
            return self._subscribed_lineups

        lineups_dict = api.get_subscribed_lineups(self._token)

        if "response" in lineups_dict and lineups_dict["response"] == "NO_LINEUPS":
            self._subscribed_lineups = []
        else:
            lineups_dict = lineups_dict["lineups"]
            self._subscribed_lineups = [Lineup.from_dict(lineup_dict) for lineup_dict in lineups_dict]

        return self._subscribed_lineups

    def add_lineup(self, lineup_id):
        response = api.add_lineup(self._token, lineup_id)
        self._subscribed_lineups = None
        return ChangeLineupResponse.from_dict(response)

    def remove_lineup(self, lineup_id):
        response = api.remove_lineup(self._token, lineup_id)
        self._subscribed_lineups = None
        return ChangeLineupResponse.from_dict(response)

    def get_lineup_map(self, lineup_id, modified=None):  # type: (...) -> LineupMap
        """

        :param lineup_id:
        :param modified:
        :return:
        """
        lineup_map = self._cache.get_lineup(lineup_id, modified)

        if lineup_map is None:
            lineup_map = api.get_lineup(self._token, lineup_id)
            self._cache.add_lineup(lineup_id, parse_datetime(lineup_map["metadata"]["modified"]), lineup_map)

        return LineupMap.from_dict(lineup_map)

    def get_lineup_map_list(self, lineups):  # type: (...) -> LineupMapList
        """

        :param lineups:
        :return:
        """
        lineup_map_list = LineupMapList()

        for lineup in lineups:
            lineup_map = self.get_lineup_map(lineup.lineup_id, lineup.modified)
            lineup_map_list.append(lineup_map)

        return lineup_map_list

    def cache_programs(self, program_hash_list):
        self._logger.debug(u"Searching for uncached programs...")

        self._cache.add_program_hashes(program_hash_list)

        programs_to_fetch = self._cache.get_program_delta()

        #self._logger.info(u"Found %s program(s) missing from cache.", len(programs_to_fetch))

        #if len(programs_to_fetch) == 0:
        #    return

        for batch in batched(programs_to_fetch, 5000):
            self._logger.info(u"Requesting %s programs from SchedulesDirect.", len(batch))
            programs = api.get_programs(self._token, batch)

            # remove (currently) unused cast and crew properties
            for program in programs:
                if "cast" in program:
                    del program["cast"]
                if "crew" in program:
                    del program["crew"]

            self._logger.info(u"Adding %s program(s) to program cache.", len(programs))
            self._cache.add_programs(programs)

    def cache_artwork(self):
        artwork_to_fetch = self._cache.get_artwork_delta()

        #self._logger.info(u"Found %s program artwork missing from cache.", len(artwork_to_fetch))

        #if len(artwork_to_fetch) == 0:
        #    return

        for batch in batched(artwork_to_fetch, 500):
            self._logger.info(u"Requesting %s program artwork from SchedulesDirect.", len(batch))
            artwork = api.get_metadata(batch)

            artwork_errors = (art for art in artwork if isinstance(art[u"data"], dict))

            for artwork_error in artwork_errors:
                self._logger.warn(u"Artwork for %s returned %s %s", artwork_error["programID"], artwork_error["data"]["errorCode"], artwork_error["data"]["errorMessage"])

            self._logger.info(u"Adding program artwork to cache.")
            self._cache.add_artwork(art for art in artwork if isinstance(art[u"data"], list))

    def refresh_cache(self, schedule_hash_set):
        with self._cache:
            changed_schedule_list = self.cache_schedules(schedule_hash_set)

            if len(changed_schedule_list) != 0:
                self.cache_programs(changed_schedule_list.get_program_hash_list())
                self._cache.update_program_max_schedule_dates(changed_schedule_list.get_program_max_schedule_dates())

            self._logger.info(u"Caching artwork...")
            self.cache_artwork()

            self._logger.info(u"Deleting expired schedules...")
            self._cache.delete_expired_schedules()

            self._logger.info(u"Deleting expired programs...")
            self._cache.delete_expired_programs()

            self._logger.info(u"Deleting expired artwork...")
            self._cache.delete_expired_artwork()

            self._logger.info(u"Compressing cache database...")
            self._cache.compress_database()

    def get_cached_programs(self, program_ids):
        return {program.program_id: program for program in self._cache.get_programs(program_ids)}

    def get_cached_artwork(self, artwork_ids):
        return {program_artwork.artwork_id: program_artwork for program_artwork in self._cache.get_artwork(artwork_ids)}

    def get_schedule_hash_list(self, station_ids):
        self._logger.info(u"Requesting schedule hashes for %s stations...", len(station_ids))
        schedule_md5s_request = [{u"stationID": station} for station in station_ids]

        result = api.get_schedule_md5s(self._token, schedule_md5s_request)

        schedule_hash_list = [(station_id, parse_date(date), result[station_id][date]["md5"]) for station_id in result for date in result[station_id]]

        return schedule_hash_list

    def cache_schedules(self, schedule_hash_list):  # type: (...) -> ScheduleList
        """

        :param schedule_hash_list:
        :return:
        """
        self._cache.add_schedule_hashes(schedule_hash_list)

        schedules_to_fetch = self._cache.get_schedule_delta()

        #self._logger.info(u"Found %s schedule(s) missing from cache.", len(schedules_to_fetch))

        schedules_request = {}
        for (station_id, schedule_date) in schedules_to_fetch:
            if station_id not in schedules_request:
                schedules_request[station_id] = []
            schedules_request[station_id].append(schedule_date.strftime("%Y-%m-%d"))

        if len(schedules_request) != 0:
            #self._logger.info(u"Requesting %s schedules from SchedulesDirect.", len(schedules_to_fetch))
            schedules_response = api.get_schedules(self._token, [{"stationID": station_id, "date": schedules_request[station_id]} for station_id in schedules_request])
            self._cache.add_schedules(schedules_response)
            return ScheduleList.from_iterable(schedules_response)

        return ScheduleList()

    def get_cached_schedules(self, schedule_keys):  # type: (...) -> ScheduleList
        """

        :param schedule_keys:
        :return:
        """
        return ScheduleList(self._cache.get_schedules(schedule_keys))

    def read_filter(self, lineup_map_list):
        import os.path
        import json
        filter = None

        if not os.path.isfile("./filter.json"):
            filter = {}

            for lineup_map in lineup_map_list:
                lineup_id = lineup_map.lineup.lineup_id
                filter[lineup_id] = {"default_import": 1}

                for channel in lineup_map.channels:
                    filter[lineup_id][channel.channel] = {"callsign": channel.station.callsign, "import": 1}

            f = open("./filter.json", "w")
            json.dump(filter, f, indent=4, sort_keys=True)
            f.close()

            return filter

        filter_changed = False
        f = open("./filter.json", "r")
        filter = json.load(f)
        f.close()

        for lineup_map in lineup_map_list:
            lineup_id = lineup_map.lineup.lineup_id

            if lineup_id not in filter:
                filter[lineup_id] = {"default_import": 1}
                filter_changed = True
            elif "default_import" not in filter[lineup_id]:
                filter[lineup_id]["default_import"] = 1
                filter_changed = True

            for channel in lineup_map.channels:
                channel_num = channel.channel

                if channel_num not in filter[lineup_id]:
                    filter[lineup_id][channel_num] = filter[lineup_id]["default_import"]
                    filter_changed = True
                elif filter[lineup_id][channel_num]["callsign"] != channel.station.callsign:
                    filter[lineup_id][channel_num]["callsign"] = channel.station.callsign
                    filter_changed = True

        if filter_changed:
            f = open("./filter.json", "w")
            json.dump(filter, f, indent=4, sort_keys=True)
            f.close()

        return filter

    def manage(self):
        while True:
            print(u"\nManage Account Options:\n")
            print(u"1. List subscribed lineups")
            print(u"2. Add lineup")
            print(u"3. Remove lineup")
            print(u"4. List lineup channels.")
            print(u"\nChoose an option or 'x' to exit.")
            choice = raw_input("> ")
            if choice == "x":
                break
            elif choice == "1":
                self._list_subscribed_lineups()
            elif choice == "2":
                self._add_lineup()
            elif choice == "3":
                self._remove_lineup()
            elif choice == "4":
                self._list_lineup_channels()

    def _list_subscribed_lineups(self):
        lineups = self.get_subscribed_lineups()
        print(u"\nSubscribed Lineups:\n")
        for lineup in lineups:
            print(u"Lineup:\t{0}".format(lineup.lineup_id))
            print(u"Name:\t{0}".format(lineup.name))
            print(u"Transport:\t{0}".format(lineup.transport))
            print(u"Location:\t{0}".format(lineup.location))
            print(u"")

    def _add_lineup(self):
        while True:
            print(u"\nAdd Lineup\n")
            print(u"Enter 3-character country/region code or 'x' to cancel:")
            country_code = raw_input("> ")
            if country_code == "x":
                break

            while True:
                print(u"Enter zip/postal code or 'x' to cancel:")
                postal_code = raw_input("> ")
                if postal_code == "x":
                    break

                headends = self.get_headends_by_postal_code(country_code, postal_code)

                while True:
                    subscribed_lineups = self.get_subscribed_lineups()
                    subscribed_lineup_ids = [lineup.lineup_id for lineup in subscribed_lineups]

                    headend_lineups = [(headend, lineup) for headend in headends for lineup in headend.lineups if lineup.lineup_id not in subscribed_lineup_ids]

                    transport_set = {headend.type for (headend, lineup) in headend_lineups}

                    options = []
                    count = 0
                    for transport in transport_set:
                        print(u"\nTransport: {0}\n".format(transport))
                        for (headend, lineup) in [(headend, lineup) for (headend, lineup) in headend_lineups if headend.type == transport]:
                            options.append((headend, lineup))
                            count += 1
                            print(u"\t{0}. {1.name} ({2.location})".format(count, lineup, headend))

                    print(u"\nChoose a lineup to add or 'x' to cancel.")
                    choice = raw_input("> ")

                    if choice == "x":
                        break

                    choice = int(choice) - 1
                    (headend, lineup) = options[choice]

                    print(u"Are you sure you want to add '{0} ({1})'? (y/n)".format(lineup.name, headend.location))
                    if raw_input("> ") != "y":
                        continue

                    response = self.add_lineup(lineup.lineup_id)

                    print(u"Schedules Direct returned '{0}'.".format(response.response_status.message))
                    print(u"{0} lineup changes remaining.\n".format(response.changes_remaining))

    def _list_lineup_channels(self):

        while True:
            print(u"\nList Lineup Channels\n")

            subscribed_lineups = self.get_subscribed_lineups()

            options = []
            count = 0
            for lineup in subscribed_lineups:
                count += 1
                options.append(lineup)
                print(u"{0}. {1.name} ({1.location})".format(count, lineup))

            print(u"\nChoose a lineup to list channels or 'x' to cancel.")
            choice = raw_input("> ")
            if choice == "x":
                break

            choice = int(choice) - 1
            lineup = options[choice]

            lineup_map = self.get_lineup_map(lineup.lineup_id)

            for channel in lineup_map.channels:
                print(u"{0}\t{1.callsign} '{1.name}'".format(channel.channel, channel.station))

    def _remove_lineup(self):

        while True:
            print(u"\nRemove Lineup\n")

            subscribed_lineups = self.get_subscribed_lineups()

            options = []
            count = 0
            for lineup in subscribed_lineups:
                count += 1
                options.append(lineup)
                print(u"{0}. {1.name} ({1.location})".format(count, lineup))

            print(u"\nChoose a lineup to remove or 'x' to cancel.")
            choice = raw_input("> ")
            if choice == "x":
                break

            choice = int(choice) - 1
            lineup = options[choice]

            print(u"Are you sure you want to remove '{0.name} ({0.location})'? (y/n)".format(lineup))
            if raw_input("> ") != "y":
                continue

            response = self.remove_lineup(lineup.lineup_id)

            print(u"\nSchedules Direct returned '{0}'.".format(response.response_status.message))
            print(u"{0} lineup changes remaining.\n".format(response.changes_remaining))
