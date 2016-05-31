import logging


class ProgramRecommendation(object):
    def __init__(self):
        self.program_id = None  # type: unicode

        self.title120 = None  # type: unicode

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[ProgramRecommendation]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(recommendation) for recommendation in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramRecommendation
        """

        :param dct:
        :return:
        """
        program_recommendation = cls()

        if "programID" in dct:
            program_recommendation.program_id = dct.pop("programID")

        if "title120" in dct:
            program_recommendation.title120 = dct.pop("title120")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramRecommendation: %s", ", ".join(dct.keys()))

        return program_recommendation
