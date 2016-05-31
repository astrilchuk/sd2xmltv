import logging


class ScheduleHash(object):
    def __init__(self, station_id, schedule_date):
        self.station_id = station_id
        """:type: unicode"""

        self.schedule_date = schedule_date
        """:type: date"""

        self.code = None
        """:type: unicode"""

        self.message = None
        """:type: unicode"""

        self.last_modified = None
        """:type: datetime"""

        self.md5 = None
        """:type: unicode"""

    def __unicode__(self):
        return u"ScheduleHash for Station {0.station_id} on {0.schedule_date}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct, station_id, schedule_date):
        """

        :param dct:
        :type dct: dict
        :param station_id:
        :type station_id: unicode
        :param schedule_date:
        :type schedule_date: date
        :return:
        :rtype: ScheduleHash
        """
        schedule_hash = cls(station_id, schedule_date)

        if "code" in dct:
            schedule_hash.code = dct.pop("code")

        if "message" in dct:
            schedule_hash.message = dct.pop("message")

        if "lastModified" in dct:
            schedule_hash.last_modified = dct.pop("lastModified")

        if "md5" in dct:
            schedule_hash.md5 = dct.pop("md5")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ScheduleMetadata: %s", ", ".join(dct.keys()))

        return schedule_hash
