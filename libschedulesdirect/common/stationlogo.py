import logging


class StationLogo(object):
    def __init__(self):
        self.url = None  # type: unicode

        self.height = None  # type: int

        self.md5 = None  # type: unicode

        self.width = None  # type: int

    def __unicode__(self):  # type: () -> unicode
        return u"Station Logo {0.width}x{0.height}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> StationLogo
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StationLogo
        """
        station_logo = cls()

        if "URL" in dct:
            station_logo.url = dct.pop("URL")

        if "height" in dct:
            station_logo.height = dct.pop("height")

        if "width" in dct:
            station_logo.width = dct.pop("width")

        if "md5" in dct:
            station_logo.md5 = dct.pop("md5")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for StationLogo: %s", ", ".join(dct.keys()))

        return station_logo
