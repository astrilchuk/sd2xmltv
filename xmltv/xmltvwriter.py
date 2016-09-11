import logging
import socket
from gzip import GzipFile


class XmltvWriter(object):
    def __init__(self, path):
        self._logger = logging.getLogger(__name__)  # type: logging.Logger
        self._path = path  # type: unicode
        self._target = None

    def __enter__(self):
        self._logger.debug(u"__enter__()")

        if self._path[-5:] == ".sock":
            self._target = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._target.connect(self._path)
        else:
            self._target = open(self._path, "wb")

            if self._path[-3:] == ".gz":
                self._target = GzipFile(fileobj=self._target)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._logger.debug(u"__exit__()")

        self._target.close()

        return False  # re-raise exception (if any)

    def write(self, data):
        if isinstance(self._target, socket.socket):
            self._target.send(data)
        else:
            self._target.write(data)
