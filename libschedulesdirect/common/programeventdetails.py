import logging
from util import parse_date
from eventteam import EventTeam


class ProgramEventDetails(object):
    def __init__(self):
        self.venue = None
        """:type: unicode"""

        self.game_date = None
        """:type: datetime"""

        self.teams = []
        """:type: list[EventTeam]"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramEventDetails
        """
        ped = cls()

        if "venue100" in dct:
            ped.venue = dct.pop("venue100")

        if "gameDate" in dct:
            ped.game_date = parse_date(dct.pop("gameDate"))

        if "teams" in dct:
            for team in dct.pop("teams"):
                ped.teams.append(EventTeam.from_dict(team))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramEventDetails: %s", ", ".join(dct.keys()))

        return ped