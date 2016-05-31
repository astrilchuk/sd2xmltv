import logging


class MultipartBroadcast(object):
    def __init__(self):
        self.part_number = None
        """:type: int"""

        self.total_parts = None
        """:type: int"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: MultipartBroadcast
        """
        multipart_broadcast = cls()

        multipart_broadcast.part_number = dct.pop("partNumber")

        multipart_broadcast.total_parts = dct.pop("totalParts")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for MultipartBroadcast: %s", ", ".join(dct.keys()))

        return multipart_broadcast
