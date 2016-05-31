import logging
from qualityrating import QualityRating


class ProgramMovie(object):
    def __init__(self):
        self.duration = None  # type: int

        self.quality_ratings = []  # type: List[QualityRating]

        self.year = None  # type: unicode

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ProgramMovie
        """

        :param dct:
        :return:
        """
        program_movie = cls()

        if "duration" in dct:
            program_movie.duration = dct.pop("duration")

        if "qualityRating" in dct:
            program_movie.quality_ratings = QualityRating.from_iterable(dct.pop("qualityRating"))

        if "year" in dct:
            program_movie.year = dct.pop("year")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramMovie: %s", ", ".join(dct.keys()))

        return program_movie
