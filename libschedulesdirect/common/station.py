import logging
from broadcaster import Broadcaster
from stationlogo import StationLogo


class Station(object):
    def __init__(self):
        self.station_id = None  # type: unicode

        self.callsign = None  # type: unicode

        self.name = None  # type: unicode

        self.affiliate = None  # type: unicode

        self.broadcast_languages = []  # type: List[unicode]

        self.description_languages = []  # type: List[unicode]

        self.broadcaster = None  # type: Broadcaster

        self.logo = None  # type: StationLogo

        self.is_commercial_free = False  # type: bool

        self.affiliate = None  # type: unicode

        self.is_radio_station = None  # type: bool

    def __unicode__(self):  # type: () -> unicode
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[Station]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(station) for station in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Station
        """

        :param dct:
        :return:
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

        if "isRadioStation" in dct:
            station.is_radio_station = dct.pop("isRadioStation")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Station: %s", ", ".join(dct.keys()))

        return station
