import logging


class ProgramCast(object):
    def __init__(self):
        self.person_id = None  # type: unicode

        self.name_id = None  # type: unicode

        self.billing_order = None  # type: unicode

        self.role = None  # type: unicode

        self.name = None  # type: unicode

        self.character_name = None  # type: unicode

    def __unicode__(self):  # type: () -> unicode
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[ProgramCast]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(cast) for cast in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramCast
        """

        :param dct:
        :return:
        """
        program_cast = cls()

        if "personId" in dct:
            program_cast.person_id = dct.pop("personId")

        if "nameId" in dct:
            program_cast.name_id = dct.pop("nameId")

        if "billingOrder" in dct:
            program_cast.billing_order = dct.pop("billingOrder")

        if "role" in dct:
            program_cast.role = dct.pop("role")

        if "name" in dct:
            program_cast.name = dct.pop("name")

        if "characterName" in dct:
            program_cast.character_name = dct.pop("characterName")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramCast: %s", ", ".join(dct.keys()))

        return program_cast
