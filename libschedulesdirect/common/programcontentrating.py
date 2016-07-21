import logging


class ProgramContentRating(object):
    def __init__(self):
        self.body = None  # type: unicode

        self.code = None  # type: unicode

        self.country = None  # type: unicode

    def __unicode__(self):  # type: () -> unicode
        return u"{0.body}: {0.code}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: Iterable[dict] -> List[ProgramContentRating]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(content_rating) for content_rating in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramContentRating
        """

        :param dct:
        :return:
        """
        program_content_rating = cls()

        if "body" in dct:
            program_content_rating.body = dct.pop("body")

        if "code" in dct:
            program_content_rating.code = dct.pop("code")

        if "country" in dct:
            program_content_rating.country = dct.pop("country")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramContentRating: %s", ", ".join(dct.keys()))

        return program_content_rating
