import logging


class ProgramTitles(object):
    def __init__(self):
        self.title120 = None  # type: unicode

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> ProgramTitles
        """

        :param iterable:
        :return:
        """
        program_titles = cls()

        for item in iterable:
            if "title120" in item:
                program_titles.title120 = item.pop("title120")
            else:
                logging.warn("Titles not processed: %s", str(item))

        return program_titles
