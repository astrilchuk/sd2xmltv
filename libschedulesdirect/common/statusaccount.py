import logging
from util import parse_datetime


class StatusAccount(object):
    def __init__(self):
        self.expires = None
        """:type: datetime"""

        self.messages = None
        """:type: list[unicode]"""

        self.max_lineups = None
        """:type: int"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StatusAccount
        """
        status_account = cls()

        if "expires" in dct:
            status_account.expires = parse_datetime(dct.pop("expires"))

        if "messages" in dct:
            status_account.messages = dct.pop("messages")

        if "maxLineups" in dct:
            status_account.max_lineups = dct.pop("maxLineups")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for StatusAccount: %s", ", ".join(dct.keys()))

        return status_account
