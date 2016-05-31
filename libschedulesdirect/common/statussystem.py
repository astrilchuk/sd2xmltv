import logging
from datetime import datetime
from util import parse_datetime


class StatusSystem(object):
    def __init__(self):
        self.date = None  # type: datetime

        self.details = None  # type: unicode

        self.status = None  # type: unicode

        self.message = None  # type: unicode

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> StatusSystem
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StatusSystem
        """
        system_status = cls()

        if "date" in dct:
            system_status.date = parse_datetime(dct.pop("date"))

        if "details" in dct:
            system_status.details = dct.pop("details")

        if "status" in dct:
            system_status.status = dct.pop("status")

        if "message" in dct:
            system_status.message = dct.pop("message")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for StatusSystem: %s", ", ".join(dct.keys()))

        return system_status
