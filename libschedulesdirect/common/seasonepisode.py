import logging


class SeasonEpisode(object):
    def __init__(self):
        self.season = None
        """:type: int"""

        self.episode = None
        """:type: int"""

        self.total_episodes = None
        """:type: int"""

        self.total_seasons = None
        """:type: int"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: SeasonEpisode
        """
        season_episode = cls()

        if "season" in dct:
            season_episode.season = dct.pop("season")

        if "episode" in dct:
            season_episode.episode = dct.pop("episode")

        if "totalEpisodes" in dct:
            season_episode.total_episodes = dct.pop("totalEpisodes")

        if "totalSeasons" in dct:
            season_episode.total_seasons = dct.pop("totalSeasons")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for SeasonEpisode: %s", ", ".join(dct.keys()))

        return season_episode
