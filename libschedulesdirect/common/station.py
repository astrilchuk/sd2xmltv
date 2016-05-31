import logging
from broadcaster import Broadcaster
from stationlogo import StationLogo


class Station(object):
    def __init__(self):
        self.station_id = None
        """:type: unicode"""

        self.callsign = None
        """:type: unicode"""

        self.name = None
        """:type: unicode"""

        self.affiliate = None
        """:type: unicode"""

        self.broadcast_languages = []
        """:type: list[unicode]"""

        self.description_languages = []
        """:type: list[unicode]"""

        self.broadcaster = None
        """:type: Broadcaster"""

        self.logo = None
        """:type: StationLogo"""

        self.is_commercial_free = False
        """:type: bool"""

        self.affiliate = None
        """:type: unicode"""

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[Station]
        """
        return [cls.from_dict(station) for station in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Station
        """
        station = cls()

        station.station_id = dct.pop("stationID")

        if "callsign" in dct:
            station.callsign = dct.pop("callsign")

        if "name" in dct:
            station.name = dct.pop("name")

        if "affiliate" in dct:
            station.affiliate = dct.pop("affiliate")

        if "broadcastLanguage" in dct:
            station.broadcast_languages = dct.pop("broadcastLanguage")

        if "descriptionLanguage" in dct:
            station.description_languages = dct.pop("descriptionLanguage")

        if "broadcaster" in dct:
            station.broadcaster = Broadcaster.from_dict(dct.pop("broadcaster"))

        if "logo" in dct:
            station.logo = StationLogo.from_dict(dct.pop("logo"))

        if "isCommercialFree" in dct:
            station.is_commercial_free = dct.pop("isCommercialFree")

        if "affiliate" in dct:
            station.affiliate = dct.pop("affiliate")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Station: %s", ", ".join(dct.keys()))

        return station
