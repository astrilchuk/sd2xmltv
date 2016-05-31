import logging
from seasonepisode import SeasonEpisode


class ProgramMetadata(object):
    def __init__(self):
        self.season_episode = None  # type: SeasonEpisode

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> ProgramMetadata
        """

        :param iterable:
        :return:
        """
        program_metadata = cls()

        for item in iterable:
            if "Gracenote" in item:
                program_metadata.season_episode = SeasonEpisode.from_dict(item.pop("Gracenote"))
            else:
                logging.warn("Program metadata not processed: %s", str(item))

        return program_metadata
