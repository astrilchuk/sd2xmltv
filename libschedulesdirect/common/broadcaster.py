import logging


class Broadcaster(object):
    def __init__(self):
        self.city = None  # type: unicode

        self.state = None  # type: unicode

        self.postalcode = None  # type: unicode

        self.country = None  # type: unicode

    def __unicode__(self):  # type: () -> unicode
        return u"Broadcaster in {0.city}, {0.state}, {0.country}, {0.postalcode}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Broadcaster
        """

        :param dct:
        :return:
        """
        broadcaster = cls()

        if "city" in dct:
            broadcaster.city = dct.pop("city")

        if "state" in dct:
            broadcaster.state = dct.pop("state")

        if "postalcode" in dct:
            broadcaster.postalcode = dct.pop("postalcode")

        if "country" in dct:
            broadcaster.country = dct.pop("country")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Broadcaster: %s", ", ".join(dct.keys()))

        return broadcaster
