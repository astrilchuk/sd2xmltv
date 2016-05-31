import logging
from responsestatus import ResponseStatus


class ChangeLineupResponse(object):
    def __init__(self):
        self.response_status = None  # type: ResponseStatus

        self.changes_remaining = None  # type: int

    def __unicode__(self):  # type: () -> unicode
        return self.response_status.message

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ChangeLineupResponse
        """

        :param dct:
        :return:
        """
        change_lineup_response = cls()

        change_lineup_response.response_status = ResponseStatus.from_dict(dct)

        if "changesRemaining" in dct:
            change_lineup_response.changes_remaining = dct.pop("changesRemaining")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ChangeLineupResponse: %s", ", ".join(dct.keys()))

        return change_lineup_response
