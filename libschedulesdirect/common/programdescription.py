import logging


class ProgramDescription(object):
    def __init__(self):
        self.text = None  # type: unicode

        self.language = None  # type: unicode

    def __unicode__(self):  # type: () -> unicode
        return self.text

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> ProgramDescription
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(description) for description in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramDescription
        """

        :param dct:
        :return:
        """
        program_description = cls()

        program_description.text = dct.pop("description")

        if "descriptionLanguage" in dct:
            program_description.language = dct.pop("descriptionLanguage")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramDescription: %s", ", ".join(dct.keys()))

        return program_description
