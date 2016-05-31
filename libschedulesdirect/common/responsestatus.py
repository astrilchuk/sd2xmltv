import logging
from datetime import datetime
from util import parse_datetime


class ResponseStatus(object):
    def __init__(self):
        self.code = None  # type: int

        self.response = None  # type: unicode

        self.message = None  # type: unicode

        self.server_id = None  # type: unicode

        self.date_time = None  # type: datetime

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ResponseStatus
        """

        :param dct:
        :return:
        """
        response_status = cls()

        if "code" in dct:
            response_status.code = dct.pop("code")
        else:
            return None

        if "response" in dct:
            response_status.response = dct.pop("response")

        if "message" in dct:
            response_status.message = dct.pop("message")

        if "serverID" in dct:
            response_status.server_id = dct.pop("serverID")

        if "datetime" in dct:
            response_status.date_time = parse_datetime(dct.pop("datetime"))

        return response_status
