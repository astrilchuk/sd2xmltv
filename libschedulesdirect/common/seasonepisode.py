import logging


class SeasonEpisode(object):
    def __init__(self):
        # Integer indicating the season number. Mandatory.
        self.season = None  # type: int

        # Integer indicating the episode number. Optional.
        self.episode = None  # type: int

        # Integer indicating the total number of episodes. Optional.
        # In an "EP" program this indicates the total number of episodes in this season.
        # In an "SH" program, it will indicate the total number of episodes in the series.
        self.total_episodes = None  # type: int

        # integer indicating the total number of seasons in the series. SH programs only. Optional.
        self.total_seasons = None  # type: int

    @property
    def has_season_episode(self):  # type: () -> bool
        return self.season is not None and self.episode is not None

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> SeasonEpisode
        """

        :param dct:
        :return:
        """
        season_episode = cls()

        if "season" in dct:
            season = dct.pop("season")
            if season != 0:
                season_episode.season = season

        if "episode" in dct:
            episode = dct.pop("episode")
            if episode != 0:
                season_episode.episode = episode

        if "totalEpisodes" in dct:
            season_episode.total_episodes = dct.pop("totalEpisodes")

        if "totalSeasons" in dct:
            season_episode.total_seasons = dct.pop("totalSeasons")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for SeasonEpisode: %s", ", ".join(dct.keys()))

        return season_episode
