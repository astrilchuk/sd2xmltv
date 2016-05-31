import logging


class ProgramCrew(object):
    def __init__(self):
        self.person_id = None  # type: unicode

        self.name_id = None  # type: unicode

        self.billing_order = None  # type: unicode

        self.role = None  # type: unicode

        self.name = None  # type: unicode

    def __unicode__(self):  # type: () -> unicode
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[ProgramCrew]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(crew) for crew in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramCrew
        """

        :param dct:
        :return:
        """
        program_crew = cls()

        if "personId" in dct:
            program_crew.person_id = dct.pop("personId")

        if "nameId" in dct:
            program_crew.name_id = dct.pop("nameId")

        if "billingOrder" in dct:
            program_crew.billing_order = dct.pop("billingOrder")

        if "role" in dct:
            program_crew.role = dct.pop("role")

        if "name" in dct:
            program_crew.name = dct.pop("name")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramCrew: %s", ", ".join(dct.keys()))

        return program_crew
