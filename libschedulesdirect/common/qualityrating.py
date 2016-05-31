import logging


class QualityRating(object):
    def __init__(self):
        self.increment = None  # type: unicode

        self.max_rating = None  # type: unicode

        self.min_rating = None  # type: unicode

        self.rating = None  # type: unicode

        self.ratings_body = None  # type: unicode

    def get_stars(self):  # type: () -> unicode
        rating_float = float(self.rating)
        rating_int = int(rating_float)
        stars_str = u"*" * rating_int  # unichr(0x2606) * rating_int
        if rating_float - rating_int > 0:
            stars_str += unichr(0x00BD)
        return stars_str

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[QualityRating]
        """

        :param iterable:
        :return:
        """
        return [QualityRating.from_dict(quality_rating) for quality_rating in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> QualityRating
        """

        :param dct:
        :return:
        """
        quality_rating = cls()

        if "increment" in dct:
            quality_rating.increment = dct.pop("increment")

        if "maxRating" in dct:
            quality_rating.max_rating = dct.pop("maxRating")

        if "minRating" in dct:
            quality_rating.min_rating = dct.pop("minRating")

        if "rating" in dct:
            quality_rating.rating = dct.pop("rating")

        if "ratingsBody" in dct:
            quality_rating.ratings_body = dct.pop("ratingsBody")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for QualityRating: %s", ", ".join(dct.keys()))

        return quality_rating
