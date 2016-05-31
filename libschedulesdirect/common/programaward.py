import logging


class ProgramAward(object):
    def __init__(self):
        self.category = None  # type: unicode

        self.award_name = None  # type: unicode

        self.name = None  # type: unicode

        self.year = None  # type: unicode

        self.recipient = None  # type: unicode

        self.won = None  # type: bool

        self.personId = None  # type: int

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[ProgramAward]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(program_award) for program_award in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramAward
        """

        :param dct:
        :return:
        """
        program_award = cls()

        if u"category" in dct:
            program_award.category = dct.pop(u"category")

        if u"awardName" in dct:
            program_award.award_name = dct.pop(u"awardName")

        if u"name" in dct:
            program_award.name = dct.pop(u"name")

        if u"year" in dct:
            program_award.year = dct.pop(u"year")

        if u"recipient" in dct:
            program_award.recipient = dct.pop(u"recipient")

        if u"won" in dct:
            program_award.won = dct.pop(u"won")

        if u"personId" in dct:
            program_award.personId = dct.pop(u"personId")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramAward: %s", ", ".join(dct.keys()))

        return program_award