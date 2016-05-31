import logging
from util import parse_datetime
from lineup import Lineup
from statusaccount import StatusAccount
from statussystem import StatusSystem


class Status(object):
    def __init__(self):
        self.account = None
        """:type: StatusAccount"""

        self.lineups = []
        """:type: list[Lineup]"""

        self.last_data_update = None
        """:type: datetime"""

        self.notifications = []
        """:type: list[unicode]"""

        self.system_status = None
        """:type: StatusSystem"""

        self.server_id = None
        """:type: unicode"""

        self.code = None
        """:type: int"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Status
        """
        status = cls()

        if "account" in dct:
            status.account = StatusAccount.from_dict(dct.pop("account"))

        if "lineups" in dct:
            status.lineups = Lineup.from_iterable(dct.pop("lineups"))

        if "lastDataUpdate" in dct:
            status.last_data_update = parse_datetime(dct.pop("lastDataUpdate"))

        if "notifications" in dct:
            status.notifications = dct.pop("notifications")

        if "systemStatus" in dct:
            if len(dct["systemStatus"]) != 0:
                status.system_status = StatusSystem.from_dict(dct.pop("systemStatus")[0])

        if "serverID" in dct:
            status.server_id = dct.pop("serverID")

        if "code" in dct:
            status.code = dct.pop("code")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Status: %s", ", ".join(dct.keys()))

        return status
