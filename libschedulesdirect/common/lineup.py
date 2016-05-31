import logging
from datetime import datetime
from util import parse_datetime


class Lineup(object):
    def __init__(self):
        self.lineup_id = None  # type: unicode

        self.name = None  # type: unicode

        self.transport = None  # type: unicode

        self.location = None  # type: unicode

        self.modified = None  # type: datetime

        self.uri = None  # type: unicode

        self.is_deleted = False  # type: bool

    def __unicode__(self):  # type: () -> unicode
        return self.lineup_id

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: Iterable[dict] -> List[Lineup]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(lineup) for lineup in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Lineup
        """

        :param dct:
        :return:
        """
        lineup = cls()

        lineup.lineup_id = dct.pop("lineup")

        if "name" in dct:
            lineup.name = dct.pop("name")

        if "transport" in dct:
            lineup.transport = dct.pop("transport")

        if "location" in dct:
            lineup.location = dct.pop("location")

        if "modified" in dct:
            lineup.modified = parse_datetime(dct.pop("modified"))

        if "uri" in dct:
            lineup.uri = dct.pop("uri")

        if "isDeleted" in dct:
            lineup.is_deleted = dct.pop("isDeleted")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Lineup: %s", ", ".join(dct.keys()))

        return lineup
