import logging
from datetime import datetime
from util import parse_date, parse_datetime


class ScheduleMetadata(object):
    def __init__(self):
        self.modified = None  # type: datetime

        self.md5 = None  # type: unicode

        self.start_date = None  # type: datetime

        self.code = None

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ScheduleMetadata
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ScheduleMetadata
        """
        schedule_metadata = cls()

        schedule_metadata.modified = parse_datetime(dct.pop("modified"))

        schedule_metadata.md5 = dct.pop("md5")

        schedule_metadata.start_date = parse_date(dct.pop("startDate"))

        # optional
        if "code" in dct:
            schedule_metadata.code = dct.pop("code")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ScheduleMetadata: %s", ", ".join(dct.keys()))

        return schedule_metadata
