import logging


class ProgramKeywords(object):
    def __init__(self):
        self.mood = None
        """:type: list[unicode]"""

        self.time_period = None
        """:type: list[unicode]"""

        self.character = None
        """:type: list[unicode]"""

        self.theme = None
        """:type: list[unicode]"""

        self.setting = None
        """:type: list[unicode]"""

        self.subject = None
        """:type: list[unicode]"""

        self.general = None
        """:type: list[unicode]"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramKeywords
        """
        program_keywords = cls()

        if "Mood" in dct:
            program_keywords.mood = dct.pop("Mood")

        if "Time Period" in dct:
            program_keywords.time_period = dct.pop("Time Period")

        if "Character" in dct:
            program_keywords.character = dct.pop("Character")

        if "Theme" in dct:
            program_keywords.theme = dct.pop("Theme")

        if "Setting" in dct:
            program_keywords.setting = dct.pop("Setting")

        if "Subject" in dct:
            program_keywords.subject = dct.pop("Subject")

        if "General" in dct:
            program_keywords.general = dct.pop("General")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramKeywords: %s", ", ".join(dct.keys()))

        return program_keywords
