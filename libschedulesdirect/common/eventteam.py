import logging


class EventTeam(object):
    def __init__(self):
        self.name = None  # type: unicode

        self.is_home = False  # type: bool

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> EventTeam
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: EventTeam
        """
        event_team = cls()

        if "name" in dct:
            event_team.name = dct.pop("name")

        if "isHome" in dct:
            event_team.is_home = dct.pop("isHome")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for EventTeam: %s", ", ".join(dct.keys()))

        return event_team
