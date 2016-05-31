import logging
from lineup import Lineup
from station import Station
from channel import Channel


class LineupMap(object):
    def __init__(self):
        self.channels = None  # type: List[Channel]

        self.stations = None  # type: List[Station]

        self.lineup = None  # type: Lineup

    def __unicode__(self):  # type: () -> unicode
        return u"LineupMap for Lineup {0.lineup_id}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> LineupMap
        """

        :param dct:
        :return:
        """
        lineup_map = cls()

        lineup_map.stations = Station.from_iterable(dct.pop("stations"))

        lineup_map.channels = Channel.from_iterable(dct.pop("map"))

        for channel in lineup_map.channels:
            channel.station = lineup_map.get_station(channel.station_id)

        lineup_map.lineup = Lineup.from_dict(dct.pop("metadata"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for LineupMap: %s", ", ".join(dct.keys()))

        return lineup_map

    def get_station(self, station_id):  # type: (unicode) -> Station
        """

        :param station_id:
        :return:
        """
        return next((station for station in self.stations if station.station_id == station_id), None)
