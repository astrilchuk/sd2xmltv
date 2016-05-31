import logging
import collections
from image import Image


class ImageList(list):
    def __init__(self, *args, **kwargs):
        super(ImageList, self).__init__(*args, **kwargs)

    def aspect_preference(self, *aspects):
        return ImageList(artwork for aspect in aspects for artwork in self if artwork.aspect == aspect)

    def category_preference(self, *categories):
        return ImageList(artwork for category in categories for artwork in self if artwork.category == category)

    def size_preference(self, *sizes):
        return ImageList(artwork for size in sizes for artwork in self if artwork.size == size)

    def tier_preference(self, *tiers):
        return ImageList(artwork for tier in tiers for artwork in self if (tier is None and artwork.tier is None) or artwork.tier == tier)

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> ImageList
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: ImageList
        """
        return cls(Image.from_iterable(iterable))
