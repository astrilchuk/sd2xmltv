import logging
from responsestatus import ResponseStatus


class Token(object):
    def __init__(self):
        self.response_status = None  # type: ResponseStatus

        self.token = None  # type: unicode

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Token
        """

        :param dct:
        :return:
        """
        token = cls()

        token.response_status = ResponseStatus.from_dict(dct)

        if "token" in dct:
            token.token = dct.pop("token")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Token: %s", ", ".join(dct.keys()))

        return token
