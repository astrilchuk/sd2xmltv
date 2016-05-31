import logging


class ProgramKeywords(object):
    def __init__(self):
        self.mood = None  # type: unicode

        self.time_period = None  # type: unicode

        self.character = None  # type: unicode

        self.theme = None  # type: unicode

        self.setting = None  # type: unicode

        self.subject = None  # type: unicode

        self.general = None  # type: unicode

    @classmethod
    def from_dict(cls, dct):  # type: dict[dict] -> ProgramKeywords
        """

        :param dct:
        :return:
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
