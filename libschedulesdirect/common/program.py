import logging
from datetime import date
from util import parse_date
from programtitles import ProgramTitles
from programeventdetails import ProgramEventDetails
from programdescriptionlist import ProgramDescriptionList
from programmetadata import ProgramMetadata
from programcast import ProgramCast
from programcrew import ProgramCrew
from programcontentrating import ProgramContentRating
from programrecommendation import ProgramRecommendation
from programmovie import ProgramMovie
from programkeywords import ProgramKeywords
from image import Image
from programaward import ProgramAward


class Program(object):
    def __init__(self):
        self.program_id = None  # type: unicode

        self.md5 = None  # type: unicode

        self.titles = None  # type: ProgramTitles

        self.event_details = None  # type: ProgramEventDetails

        self.descriptions = None  # type: ProgramDescriptionList

        self.original_air_date = None  # type: date

        self.genres = []  # type: List[unicode]

        self.episode_title = None  # type: unicode

        self.metadata = None  # type: ProgramMetadata

        self.cast = []  # type: List[ProgramCast]

        self.crew = []  # type: List[ProgramCrew]

        self.show_type = None  # type: unicode

        self.has_image_artwork = False  # type: bool

        self.content_ratings = []  # type: List[ProgramContentRating]

        self.content_advisories = []  # type: List[unicode]

        self.recommendations = []  # type: List[ProgramRecommendation]

        self.movie = None  # type: ProgramMovie

        self.episode_num = None  # type: int

        self.animation = None  # type: unicode

        self.audience = None  # type: unicode

        self.holiday = None  # type: unicode

        self.keywords = None  # type: ProgramKeywords

        self.official_url = None  # type: unicode

        self.entity_type = None  # type: unicode

        self.resource_id = None  # type: unicode

        self.episode_image = None  # type: Image

        self.duration = None  # type: int

        self.awards = None  # type: List[ProgramAward]

    @property
    def artwork_id(self):  # type: () -> unicode
        if not self.has_image_artwork:
            return None
        return self.program_id[0:10]

    @property
    def is_show_entity(self):  # type: () -> bool
        return self.entity_type == u"Show"

    @property
    def is_episode_entity(self):  # type: () -> bool
        return self.entity_type == u"Episode"

    @property
    def is_movie_entity(self):  # type: () -> bool
        return self.entity_type == u"Movie"

    @property
    def is_sports_entity(self):  # type: () -> bool
        return self.entity_type == u"Sports"

    def __unicode__(self):  # type: () -> unicode
        return u"{0.program_id} '{1.title120}'".format(self, self.titles)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def get_content_rating(self, body):
        return next((content_rating for content_rating in self.content_ratings if content_rating.body == body), None)

    def get_cast(self, in_roles):  # type: (List[unicode]) -> List[ProgramCast]
        return [cast for cast in self.cast if cast.role in in_roles]

    def get_crew(self, in_roles):  # type: (List[unicode]) -> List[ProgramCrew]
        return [crew for crew in self.crew if crew.role in in_roles]

    @staticmethod
    def from_dict(dct):  # type: (dict) -> Program
        """

        :param dct:
        :return:
        """
        if "programID" not in dct or "md5" not in dct:
            return dct

        program = Program()

        program.program_id = dct.pop("programID")

        if program.program_id[:2] == "EP":
            program.episode_num = int(program.program_id[-4:])

        program.titles = ProgramTitles.from_iterable(dct.pop("titles"))

        program.md5 = dct.pop("md5")

        if "eventDetails" in dct:
            program.event_details = ProgramEventDetails.from_dict(dct.pop("eventDetails"))

        if "descriptions" in dct:
            program.descriptions = ProgramDescriptionList.from_dict(dct.pop("descriptions"))

        if "originalAirDate" in dct:
            program.original_air_date = parse_date(dct.pop("originalAirDate"))

        if "genres" in dct:
            program.genres = dct.pop("genres")

        if "episodeTitle150" in dct:
            program.episode_title = dct.pop("episodeTitle150")

        if "metadata" in dct:
            program.metadata = ProgramMetadata.from_iterable(dct.pop("metadata"))

        if "cast" in dct:
            program.cast = ProgramCast.from_iterable(dct.pop("cast"))

        if "crew" in dct:
            program.crew = ProgramCrew.from_iterable(dct.pop("crew"))

        if "showType" in dct:
            program.show_type = dct.pop("showType")

        if "hasImageArtwork" in dct:
            program.has_image_artwork = dct.pop("hasImageArtwork")

        if "contentRating" in dct:
            program.content_ratings = ProgramContentRating.from_iterable(dct.pop("contentRating"))

        if "contentAdvisory" in dct:
            program.content_advisories = dct.pop("contentAdvisory")

        if "recommendations" in dct:
            program.recommendations = ProgramRecommendation.from_iterable(dct.pop("recommendations"))

        if "movie" in dct:
            program.movie = ProgramMovie.from_dict(dct.pop("movie"))

        if "animation" in dct:
            program.animation = dct.pop("animation")

        if "audience" in dct:
            program.audience = dct.pop("audience")

        if "holiday" in dct:
            program.holiday = dct.pop("holiday")

        if "keyWords" in dct:
            program.keywords = ProgramKeywords.from_dict(dct.pop("keyWords"))

        if "officialURL" in dct:
            program.official_url = dct.pop("officialURL")

        if "entityType" in dct:
            program.entity_type = dct.pop("entityType")

        if "resourceID" in dct:
            program.resource_id = dct.pop("resourceID")

        if "episodeImage" in dct:
            program.episode_image = Image.from_dict(dct.pop("episodeImage"))

        if "duration" in dct:
            program.duration = dct.pop("duration")

        if "awards" in dct:
            program.awards = ProgramAward.from_iterable(dct.pop("awards"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Program: %s", ", ".join(dct.keys()))

        return program
