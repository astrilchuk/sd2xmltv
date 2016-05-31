import logging
import collections
from imagelist import ImageList


class ProgramArtwork(object):
    def __init__(self):
        self.artwork_id = None
        """:type: unicode"""

        self.image_list = ImageList()
        """:type: ImageList"""

    @staticmethod
    def from_dict(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramArtwork
        """
        if "programID" not in dct:
            return dct

        program_artwork = ProgramArtwork()

        program_artwork.artwork_id = dct.pop("programID")

        program_artwork.image_list = ImageList.from_iterable(dct.pop("data"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramArtwork: %s", ", ".join(dct.keys()))

        return program_artwork

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: ProgramArtwork
        """
        return [ProgramArtwork.from_dict(item) for item in iterable]
