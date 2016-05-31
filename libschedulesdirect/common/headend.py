import logging
from lineup import Lineup


class Headend(object):
    def __init__(self):
        self.headend_id = None  # type: unicode

        self.transport = None  # type: unicode

        self.location = None  # type: unicode

        self.lineups = []  # type: List[Lineup]

    def __unicode__(self):  # type: () -> unicode
        return u"{0.headend_id} / {0.transport} / {0.location}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Headend
        """

        :param dct:
        :return:
        """
        headend = cls()

        headend.headend_id = dct.pop("headend")

        headend.type = dct.pop("transport")

        headend.location = dct.pop("location")

        headend.lineups = Lineup.from_iterable(dct.pop("lineups"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Headend: %s", ", ".join(dct.keys()))

        return headend
