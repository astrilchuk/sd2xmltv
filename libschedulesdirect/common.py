#!/usr/bin/python
# coding=utf-8

from datetime import date, datetime, timedelta
from . import parse_date, parse_datetime, unique
import logging
import collections


class ResponseStatus(object):
    def __init__(self):
        self.code = None
        """:type: int"""

        self.response = None
        """:type: unicode"""

        self.message = None
        """:type: unicode"""

        self.server_id = None
        """:type: unicode"""

        self.date_time = None
        """:type: datetime"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ResponseStatus
        """
        response_status = cls()

        if "code" in dct:
            response_status.code = dct.pop("code")
        else:
            return None

        if "response" in dct:
            response_status.response = dct.pop("response")

        if "message" in dct:
            response_status.message = dct.pop("message")

        if "serverID" in dct:
            response_status.server_id = dct.pop("serverID")

        if "datetime" in dct:
            response_status.date_time = parse_datetime(dct.pop("datetime"))

        return response_status


class Token(object):
    def __init__(self):
        self.response_status = None
        """:type: ResponseStatus"""

        self.token = None
        """:type: unicode"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Token
        """
        token = cls()

        token.response_status = ResponseStatus.from_dict(dct)

        if "token" in dct:
            token.token = dct.pop("token")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Token: %s", ", ".join(dct.keys()))

        return token


class StatusAccount(object):
    def __init__(self):
        self.expires = None
        """:type: datetime"""

        self.messages = None
        """:type: list[unicode]"""

        self.max_lineups = None
        """:type: int"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StatusAccount
        """
        status_account = cls()

        if "expires" in dct:
            status_account.expires = parse_datetime(dct.pop("expires"))

        if "messages" in dct:
            status_account.messages = dct.pop("messages")

        if "maxLineups" in dct:
            status_account.max_lineups = dct.pop("maxLineups")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for StatusAccount: %s", ", ".join(dct.keys()))

        return status_account


class StatusSystem(object):
    def __init__(self):
        self.date = None
        """:type: datetime"""

        self.details = None
        """:type: unicode"""

        self.status = None
        """:type: unicode"""

        self.message = None
        """:type: unicode"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StatusSystem
        """
        system_status = cls()

        if "date" in dct:
            system_status.date = parse_datetime(dct.pop("date"))

        if "details" in dct:
            system_status.details = dct.pop("details")

        if "status" in dct:
            system_status.status = dct.pop("status")

        if "message" in dct:
            system_status.message = dct.pop("message")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for StatusSystem: %s", ", ".join(dct.keys()))

        return system_status


class Status(object):
    def __init__(self):
        self.account = None
        """:type: StatusAccount"""

        self.lineups = []
        """:type: list[Lineup]"""

        self.last_data_update = None
        """:type: datetime"""

        self.notifications = []
        """:type: list[unicode]"""

        self.system_status = None
        """:type: StatusSystem"""

        self.server_id = None
        """:type: unicode"""

        self.code = None
        """:type: int"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Status
        """
        status = cls()

        if "account" in dct:
            status.account = StatusAccount.from_dict(dct.pop("account"))

        if "lineups" in dct:
            status.lineups = Lineup.from_iterable(dct.pop("lineups"))

        if "lastDataUpdate" in dct:
            status.last_data_update = parse_datetime(dct.pop("lastDataUpdate"))

        if "notifications" in dct:
            status.notifications = dct.pop("notifications")

        if "systemStatus" in dct:
            if len(dct["systemStatus"]) != 0:
                status.system_status = StatusSystem.from_dict(dct.pop("systemStatus")[0])

        if "serverID" in dct:
            status.server_id = dct.pop("serverID")

        if "code" in dct:
            status.code = dct.pop("code")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Status: %s", ", ".join(dct.keys()))

        return status


class ChangeLineupResponse(object):
    def __init__(self):
        self.response_status = None
        """:type: ResponseStatus"""

        self.changes_remaining = None
        """:type: int"""

    def __unicode__(self):
        return self.response_status.message

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ChangeLineupResponse
        """
        change_lineup_response = cls()

        change_lineup_response.response_status = ResponseStatus.from_dict(dct)

        if "changesRemaining" in dct:
            change_lineup_response.changes_remaining = dct.pop("changesRemaining")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ChangeLineupResponse: %s", ", ".join(dct.keys()))

        return change_lineup_response


class Lineup(object):
    def __init__(self):
        self.lineup_id = None
        """:type: unicode"""

        self.name = None
        """:type: unicode"""

        self.transport = None
        """:type: unicode"""

        self.location = None
        """:type: unicode"""

        self.modified = None
        """:type: datetime"""

        self.uri = None
        """:type: unicode"""

        self.is_deleted = False
        """:type: bool"""

    def __unicode__(self):
        return self.lineup_id

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[Lineup]
        """
        return [cls.from_dict(lineup) for lineup in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Lineup
        """
        lineup = cls()

        lineup.lineup_id = dct.pop("lineup")

        if "name" in dct:
            lineup.name = dct.pop("name")

        if "transport" in dct:
            lineup.transport = dct.pop("transport")

        if "location" in dct:
            lineup.location = dct.pop("location")

        if "modified" in dct:
            lineup.modified = parse_datetime(dct.pop("modified"))

        if "uri" in dct:
            lineup.uri = dct.pop("uri")

        if "isDeleted" in dct:
            lineup.is_deleted = dct.pop("isDeleted")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Lineup: %s", ", ".join(dct.keys()))

        return lineup


class Headend(object):
    def __init__(self):
        self.headend_id = None
        """:type: unicode"""

        self.transport = None
        """:type: unicode"""

        self.location = None
        """:type: unicode"""

        self.lineups = []
        """:type: list[Lineup]"""

    def __unicode__(self):
        return u"{0.headend_id} / {0.transport} / {0.location}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Headend
        """
        headend = cls()

        headend.headend_id = dct.pop("headend")

        headend.type = dct.pop("transport")

        headend.location = dct.pop("location")

        headend.lineups = Lineup.from_iterable(dct.pop("lineups"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Headend: %s", ", ".join(dct.keys()))

        return headend


class LineupMap(object):
    def __init__(self):
        self.channels = None
        """:type: list[Channel]"""

        self.stations = None
        """:type: list[Station]"""

        self.lineup = None
        """:type: Lineup"""

    def __unicode__(self):
        return u"LineupMap for Lineup {0.lineup_id}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: LineupMap
        """
        lineup_map = cls()

        lineup_map.stations = Station.from_iterable(dct.pop("stations"))

        lineup_map.channels = Channel.from_iterable(dct.pop("map"))

        for channel in lineup_map.channels:
            channel.station = lineup_map.get_station(channel.station_id)

        lineup_map.lineup = Lineup.from_dict(dct.pop("metadata"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for LineupMap: %s", ", ".join(dct.keys()))

        return lineup_map

    def get_station(self, station_id):
        """

        :param station_id:
        :type station_id: unicode
        :return:
        :rtype: Station
        """
        return next((station for station in self.stations if station.station_id == station_id), None)


class LineupMapList(list):
    def __init__(self, *args, **kwargs):
        super(LineupMapList, self).__init__(*args, **kwargs)

    def unique_channels(self, channel_filter=None):
        return unique((channel
                       for lineup_map in self
                       for channel in lineup_map.channels
                       if channel_filter is None or channel.channel in channel_filter), lambda c: c.get_unique_id())

    def unique_stations(self, channel_filter=None):
        return unique((channel.station
                       for channel in self.unique_channels(channel_filter)), lambda s: s.station_id)


class Channel(object):
    def __init__(self):
        # Common
        self.station_id = None
        """:type: unicode"""

        self.station = None
        """:type: Station"""

        self.channel = None
        """:type: unicode"""

        # Antenna
        self.atsc_major = None
        """:type: int"""

        self.atsc_minor = None
        """:type: int"""

        self.uhf_vhf = None
        """:type: int"""

        # DVB-T/C/S

        self.frequency_hz = None
        """:type: int"""

        self.delivery_system = None
        """:type: unicode"""

        self.modulation_system = None
        """:type: unicode"""

        self.symbol_rate = None
        """:type: int"""

        self.service_id = None
        """:type: int"""

        self.network_id = None
        """:type: int"""

        self.transport_id = None
        """:type: int"""

        self.polarization = None
        """:type: unicode"""

        self.fec = None
        """:type: unicode"""

    def get_display_names(self):
        if self.channel is not None:
            yield u"{0.channel} {1.callsign}".format(self, self.station)
            yield self.channel

        if self.uhf_vhf is not None:
            yield u"{0.uhf_vhf} {1.callsign} fcc".format(self, self.station)

        yield self.station.callsign
        yield self.station.name

    def get_unique_id(self):
        return "I{0.channel}.{0.station_id}.schedulesdirect.org".format(self)

    def __unicode__(self):
        return u"Channel {0.channel}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[Channel]
        """
        return [cls.from_dict(channel) for channel in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Channel
        """
        channel = cls()

        channel.station_id = dct.pop("stationID")

        if "channel" in dct:
            channel.channel = dct.pop("channel")

        # Antenna

        if "atscMajor" in dct:
            channel.atsc_major = dct.pop("atscMajor")

        if "atscMinor" in dct:
            channel.atsc_minor = dct.pop("atscMinor")

        if "uhfVhf" in dct:
            channel.uhf_vhf = dct.pop("uhfVhf")

        if channel.channel is None and channel.atsc_major is not None and channel.atsc_minor is not None:
            channel.channel = u"{0.atsc_major}.{0.atsc_minor}".format(channel)

        if channel.channel is None and channel.uhf_vhf is not None:
            channel.channel = str(channel.uhf_vhf)

        # DVB-T/C/S

        if "frequencyHz" in dct:
            channel.frequency_hz = dct.pop("frequencyHz")

        if "deliverySystem" in dct:
            channel.delivery_system = dct.pop("deliverySystem")

        if "modulationSystem" in dct:
            channel.modulation_system = dct.pop("modulationSystem")

        if "symbolrate" in dct:
            channel.symbol_rate = dct.pop("symbolrate")

        if "serviceID" in dct:
            channel.service_id = dct.pop("serviceID")

        if "networkID" in dct:
            channel.network_id = dct.pop("networkID")

        if "transportID" in dct:
            channel.transport_id = dct.pop("transportID")

        if "polarization" in dct:
            channel.polarization = dct.pop("polarization")

        if "fec" in dct:
            channel.fec = dct.pop("fec")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Channel: %s", ", ".join(dct.keys()))

        return channel


class Broadcaster(object):
    def __init__(self):
        self.city = None
        """:type: unicode"""

        self.state = None
        """:type: unicode"""

        self.postalcode = None
        """:type: unicode"""

        self.country = None
        """:type: unicode"""

    def __unicode__(self):
        return u"Broadcaster in {0.city}, {0.state}, {0.country}, {0.postalcode}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Broadcaster
        """
        broadcaster = cls()

        if "city" in dct:
            broadcaster.city = dct.pop("city")

        if "state" in dct:
            broadcaster.state = dct.pop("state")

        if "postalcode" in dct:
            broadcaster.postalcode = dct.pop("postalcode")

        if "country" in dct:
            broadcaster.country = dct.pop("country")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Broadcaster: %s", ", ".join(dct.keys()))

        return broadcaster


class StationLogo(object):
    def __init__(self):
        self.url = None
        """:type: unicode"""

        self.height = None
        """:type: int"""

        self.md5 = None
        """:type: unicode"""

        self.width = None
        """:type: int"""

    def __unicode__(self):
        return u"Station Logo {0.width}x{0.height}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StationLogo
        """
        station_logo = cls()

        if "URL" in dct:
            station_logo.url = dct.pop("URL")

        if "height" in dct:
            station_logo.height = dct.pop("height")

        if "width" in dct:
            station_logo.width = dct.pop("width")

        if "md5" in dct:
            station_logo.md5 = dct.pop("md5")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for StationLogo: %s", ", ".join(dct.keys()))

        return station_logo


class Station(object):
    def __init__(self):
        self.station_id = None
        """:type: unicode"""

        self.callsign = None
        """:type: unicode"""

        self.name = None
        """:type: unicode"""

        self.affiliate = None
        """:type: unicode"""

        self.broadcast_languages = []
        """:type: list[unicode]"""

        self.description_languages = []
        """:type: list[unicode]"""

        self.broadcaster = None
        """:type: Broadcaster"""

        self.logo = None
        """:type: StationLogo"""

        self.is_commercial_free = False
        """:type: bool"""

        self.affiliate = None
        """:type: unicode"""

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[Station]
        """
        return [cls.from_dict(station) for station in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Station
        """
        station = cls()

        station.station_id = dct.pop("stationID")

        if "callsign" in dct:
            station.callsign = dct.pop("callsign")

        if "name" in dct:
            station.name = dct.pop("name")

        if "affiliate" in dct:
            station.affiliate = dct.pop("affiliate")

        if "broadcastLanguage" in dct:
            station.broadcast_languages = dct.pop("broadcastLanguage")

        if "descriptionLanguage" in dct:
            station.description_languages = dct.pop("descriptionLanguage")

        if "broadcaster" in dct:
            station.broadcaster = Broadcaster.from_dict(dct.pop("broadcaster"))

        if "logo" in dct:
            station.logo = StationLogo.from_dict(dct.pop("logo"))

        if "isCommercialFree" in dct:
            station.is_commercial_free = dct.pop("isCommercialFree")

        if "affiliate" in dct:
            station.affiliate = dct.pop("affiliate")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Station: %s", ", ".join(dct.keys()))

        return station


class ProgramTitles(object):
    def __init__(self):
        self.title120 = None
        """:type: unicode"""

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: ProgramTitles
        """
        program_titles = cls()

        for item in iterable:
            if "title120" in item:
                program_titles.title120 = item.pop("title120")
            else:
                logging.warn("Titles not processed: %s", str(item))

        return program_titles


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


class ProgramMetadata(object):
    def __init__(self):
        self.season_episode = None
        """:type : SeasonEpisode"""

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: ProgramMetadata
        """
        program_metadata = cls()

        for item in iterable:
            if "Gracenote" in item:
                program_metadata.season_episode = SeasonEpisode.from_dict(item.pop("Gracenote"))
            else:
                logging.warn("Program metadata not processed: %s", str(item))

        return program_metadata


class ProgramDescription(object):
    def __init__(self):
        self.text = None
        """:type: unicode"""

        self.language = None
        """:type: unicode"""

    def __unicode__(self):
        return self.text

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[ProgramDescription]
        """
        return [cls.from_dict(description) for description in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramDescription
        """
        program_description = cls()

        program_description.text = dct.pop("description")

        if "descriptionLanguage" in dct:
            program_description.language = dct.pop("descriptionLanguage")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramDescription: %s", ", ".join(dct.keys()))

        return program_description


class ProgramDescriptionList(list):
    def __init__(self, *args, **kwargs):
        super(ProgramDescriptionList, self).__init__(*args, **kwargs)

    def languages(self):
        return list({description.language for description in self})

    def ordered_by_text_length(self, reverse=False):
        return sorted(self, key=lambda description: len(description.text), reverse=reverse)

    def get_shortest_text(self, language="en"):
        return next((description.text for description in self.ordered_by_text_length(False) if description.language == language), None)

    def get_longest_text(self, language="en"):
        return next((description.text for description in self.ordered_by_text_length(True) if description.language == language), None)

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramDescriptionList
        """
        program_description_list = cls()

        if "description100" in dct:
            program_description_list.extend(ProgramDescription.from_iterable(dct.pop("description100")))

        if "description1000" in dct:
            program_description_list.extend(ProgramDescription.from_iterable(dct.pop("description1000")))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramDescriptions: %s", ", ".join(dct.keys()))

        return program_description_list


class QualityRating(object):
    def __init__(self):
        self.increment = None
        """:type: unicode"""

        self.max_rating = None
        """:type: unicode"""

        self.min_rating = None
        """:type: unicode"""

        self.rating = None
        """:type: unicode"""

        self.ratings_body = None
        """:type: unicode"""

    def get_stars(self):
        rating_float = float(self.rating)
        rating_int = int(rating_float)
        stars_str = u"*" * rating_int  # unichr(0x2606) * rating_int
        if rating_float - rating_int > 0:
            stars_str += unichr(0x00BD)
        return stars_str

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[QualityRating]
        """
        return [QualityRating.from_dict(quality_rating) for quality_rating in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: QualityRating
        """
        quality_rating = cls()

        if "increment" in dct:
            quality_rating.increment = dct.pop("increment")

        if "maxRating" in dct:
            quality_rating.max_rating = dct.pop("maxRating")

        if "minRating" in dct:
            quality_rating.min_rating = dct.pop("minRating")

        if "rating" in dct:
            quality_rating.rating = dct.pop("rating")

        if "ratingsBody" in dct:
            quality_rating.ratings_body = dct.pop("ratingsBody")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for QualityRating: %s", ", ".join(dct.keys()))

        return quality_rating


class ProgramMovie(object):
    def __init__(self):
        self.duration = None
        """:type: int"""

        self.quality_ratings = []
        """:type: list[QualityRating]"""

        self.year = None
        """:type: unicode"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramMovie
        """
        program_movie = cls()

        if "duration" in dct:
            program_movie.duration = dct.pop("duration")

        if "qualityRating" in dct:
            program_movie.quality_ratings = QualityRating.from_iterable(dct.pop("qualityRating"))

        if "year" in dct:
            program_movie.year = dct.pop("year")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramMovie: %s", ", ".join(dct.keys()))

        return program_movie


class ProgramContentRating(object):
    def __init__(self):
        self.body = None
        """:type: unicode"""

        self.code = None
        """:type: unicode"""

    def __unicode__(self):
        return u"{0.body}: {0.code}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[ProgramContentRating]
        """
        return [cls.from_dict(content_rating) for content_rating in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramContentRating
        """
        program_content_rating = cls()

        if "body" in dct:
            program_content_rating.body = dct.pop("body")

        if "code" in dct:
            program_content_rating.code = dct.pop("code")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramContentRating: %s", ", ".join(dct.keys()))

        return program_content_rating


class ProgramRecommendation(object):
    def __init__(self):
        self.program_id = None
        """:type: unicode"""

        self.title120 = None
        """:type: unicode"""

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: ProgramRecommendation
        """
        return [cls.from_dict(recommendation) for recommendation in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramRecommendation
        """
        program_recommendation = cls()

        if "programID" in dct:
            program_recommendation.program_id = dct.pop("programID")

        if "title120" in dct:
            program_recommendation.title120 = dct.pop("title120")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramRecommendation: %s", ", ".join(dct.keys()))

        return program_recommendation


class ProgramCast(object):
    def __init__(self):
        self.person_id = None
        """:type: unicode"""

        self.name_id = None
        """:type: unicode"""

        self.billing_order = None
        """:type: unicode"""

        self.role = None
        """:type: unicode"""

        self.name = None
        """:type: unicode"""

        self.character_name = None
        """:type: unicode"""

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[ProgramCast]
        """
        return [cls.from_dict(cast) for cast in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramCast
        """
        program_cast = cls()

        if "personId" in dct:
            program_cast.person_id = dct.pop("personId")

        if "nameId" in dct:
            program_cast.name_id = dct.pop("nameId")

        if "billingOrder" in dct:
            program_cast.billing_order = dct.pop("billingOrder")

        if "role" in dct:
            program_cast.role = dct.pop("role")

        if "name" in dct:
            program_cast.name = dct.pop("name")

        if "characterName" in dct:
            program_cast.character_name = dct.pop("characterName")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramCast: %s", ", ".join(dct.keys()))

        return program_cast


class ProgramCrew(object):
    def __init__(self):
        self.person_id = None
        """:type: unicode"""

        self.name_id = None
        """:type: unicode"""

        self.billing_order = None
        """:type: unicode"""

        self.role = None
        """:type: unicode"""

        self.name = None
        """:type: unicode"""

    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[ProgramCrew]
        """
        return [cls.from_dict(crew) for crew in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramCrew
        """
        program_crew = cls()

        if "personId" in dct:
            program_crew.person_id = dct.pop("personId")

        if "nameId" in dct:
            program_crew.name_id = dct.pop("nameId")

        if "billingOrder" in dct:
            program_crew.billing_order = dct.pop("billingOrder")

        if "role" in dct:
            program_crew.role = dct.pop("role")

        if "name" in dct:
            program_crew.name = dct.pop("name")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramCrew: %s", ", ".join(dct.keys()))

        return program_crew


class EventTeam(object):
    def __init__(self):
        self.name = None
        """:type: unicode"""

        self.is_home = False
        """:type: bool"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: EventTeam
        """
        event_team = cls()

        if "name" in dct:
            event_team.name = dct.pop("name")

        if "isHome" in dct:
            event_team.is_home = dct.pop("isHome")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for EventTeam: %s", ", ".join(dct.keys()))

        return event_team


class ProgramEventDetails(object):
    def __init__(self):
        self.venue = None
        """:type: unicode"""

        self.game_date = None
        """:type: datetime"""

        self.teams = []
        """:type: list[EventTeam]"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramEventDetails
        """
        ped = cls()

        if "venue100" in dct:
            ped.venue = dct.pop("venue100")

        if "gameDate" in dct:
            ped.game_date = parse_date(dct.pop("gameDate"))

        if "teams" in dct:
            for team in dct.pop("teams"):
                ped.teams.append(EventTeam.from_dict(team))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramEventDetails: %s", ", ".join(dct.keys()))

        return ped


class ProgramKeywords(object):
    def __init__(self):
        self.mood = None
        """:type: list[unicode]"""

        self.time_period = None
        """:type: list[unicode]"""

        self.character = None
        """:type: list[unicode]"""

        self.theme = None
        """:type: list[unicode]"""

        self.setting = None
        """:type: list[unicode]"""

        self.subject = None
        """:type: list[unicode]"""

        self.general = None
        """:type: list[unicode]"""

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramKeywords
        """
        program_keywords = cls()

        if "Mood" in dct:
            program_keywords.mood = dct.pop("Mood")

        if "Time Period" in dct:
            program_keywords.time_period = dct.pop("Time Period")

        if "Character" in dct:
            program_keywords.character = dct.pop("Character")

        if "Theme" in dct:
            program_keywords.theme = dct.pop("Theme")

        if "Setting" in dct:
            program_keywords.setting = dct.pop("Setting")

        if "Subject" in dct:
            program_keywords.subject = dct.pop("Subject")

        if "General" in dct:
            program_keywords.general = dct.pop("General")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ProgramKeywords: %s", ", ".join(dct.keys()))

        return program_keywords

class Program(object):
    def __init__(self):
        self.program_id = None
        """:type: unicode"""

        self.md5 = None
        """:type: unicode"""

        self.titles = None
        """:type: ProgramTitles"""

        self.event_details = None
        """:type: ProgramEventDetails"""

        self.descriptions = None
        """:type: ProgramDescriptionList"""

        self.original_air_date = None
        """:type: date"""

        self.genres = []
        """:type: list[unicode]"""

        self.episode_title = None
        """:type: unicode"""

        self.metadata = None
        """:type: ProgramMetadata"""

        self.cast = []
        """:type: list[ProgramCast]"""

        self.crew = []
        """:type: list[ProgramCrew]"""

        self.show_type = None
        """:type: unicode"""

        self.has_image_artwork = False
        """:type: bool"""

        self.content_ratings = []
        """:type: list[ProgramContentRating]"""

        self.content_advisories = []
        """:type: list[unicode]"""

        self.recommendations = []
        """:type: list[ProgramRecommendation]"""

        self.movie = None
        """:type: ProgramMovie"""

        self.episode_num = None
        """:type: int"""

        self.animation = None
        """:type: unicode"""

        self.audience = None
        """:type: unicode"""

        self.holiday = None
        """:type: unicode"""

        self.keywords = None
        """:type: ProgramKeywords"""

        self.official_url = None
        """:type: unicode"""

        self.entity_type = None
        """:type: unicode"""

        self.resource_id = None
        """:type: unicode"""

    @property
    def artwork_id(self):
        if not self.has_image_artwork:
            return None
        return self.program_id[0:10]

    @property
    def is_show_entity(self):
        return self.entity_type == u"Show"

    @property
    def is_episode_entity(self):
        return self.entity_type == u"Episode"

    @property
    def is_movie_entity(self):
        return self.entity_type == u"Movie"

    @property
    def is_sports_entity(self):
        return self.entity_type == u"Sports"

    def __unicode__(self):
        return u"{0.program_id} '{1.title120}'".format(self, self.titles)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def get_content_rating(self, body):
        return next((content_rating for content_rating in self.content_ratings if content_rating.body == body), None)

    def get_cast(self, in_roles):
        return [cast for cast in self.cast if cast.role in in_roles]

    def get_crew(self, in_roles):
        return [crew for crew in self.crew if crew.role in in_roles]

    @staticmethod
    def from_dict(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Program
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

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Program: %s", ", ".join(dct.keys()))

        return program


class ScheduleHashList(list):
    def __init__(self, *args, **kwargs):
        super(ScheduleHashList, self).__init__(*args, **kwargs)

    def schedule_dates(self):
        return sorted({schedule_hash.schedule_date for schedule_hash in self})

    def get_station_id_set(self):
        return {schedule_hash.station_id for schedule_hash in self}

    def get_schedule_hashes(self):
        return [(item.station_id, item.schedule_date, item.md5) for item in self]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ScheduleHashList
        """
        return cls([ScheduleHash.from_dict(dct[station_id][schedule_date], station_id, parse_date(schedule_date)) for station_id in dct for schedule_date in dct[station_id]])


class ScheduleHash(object):
    def __init__(self, station_id, schedule_date):
        self.station_id = station_id
        """:type: unicode"""

        self.schedule_date = schedule_date
        """:type: date"""

        self.code = None
        """:type: unicode"""

        self.message = None
        """:type: unicode"""

        self.last_modified = None
        """:type: datetime"""

        self.md5 = None
        """:type: unicode"""

    def __unicode__(self):
        return u"ScheduleHash for Station {0.station_id} on {0.schedule_date}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct, station_id, schedule_date):
        """

        :param dct:
        :type dct: dict
        :param station_id:
        :type station_id: unicode
        :param schedule_date:
        :type schedule_date: date
        :return:
        :rtype: ScheduleHash
        """
        schedule_hash = cls(station_id, schedule_date)

        if "code" in dct:
            schedule_hash.code = dct.pop("code")

        if "message" in dct:
            schedule_hash.message = dct.pop("message")

        if "lastModified" in dct:
            schedule_hash.last_modified = dct.pop("lastModified")

        if "md5" in dct:
            schedule_hash.md5 = dct.pop("md5")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ScheduleMetadata: %s", ", ".join(dct.keys()))

        return schedule_hash


class ScheduleList(list):
    def __init__(self, *args, **kwargs):
        super(ScheduleList, self).__init__(*args, **kwargs)

    def schedule_dates(self):
        return sorted({schedule.metadata.start_date for schedule in self})

    def order_by(self, sort_func):
        return (schedule for schedule in sorted(self, key=sort_func))

    def order_by_start_date(self):
        return self.order_by(lambda schedule: schedule.metadata.start_date)

    def get_broadcasts(self):
        for schedule in self:
            for broadcast in schedule.broadcasts:
                yield broadcast

    def get_program_ids(self):
        return unique(broadcast.program_id for schedule in self for broadcast in schedule.broadcasts)

    def get_program_hash_list(self):
        return list({(broadcast.program_id, broadcast.md5) for schedule in self for broadcast in schedule.broadcasts})

    def get_program_max_schedule_dates(self):
        return [(program_id, max_schedule_date) for program_id, max_schedule_date in {broadcast.program_id: schedule.metadata.start_date for schedule in self.order_by_start_date() for broadcast in schedule.broadcasts}.iteritems()]

    def get_schedule(self, station_id, schedule_date):
        """

        :param station_id:
        :type station_id: unicode
        :param schedule_date:
        :type schedule_date: date
        :return:
        :rtype: Schedule
        """
        return next((schedule for schedule in self if schedule.station_id == station_id and schedule.metadata.start_date == schedule_date), None)

    @staticmethod
    def from_iterable(iterable):
        return ScheduleList([Schedule.from_dict(item) for item in iterable])


class ScheduleMetadata(object):
    def __init__(self):
        self.modified = None
        """:type: datetime"""

        self.md5 = None
        """:type: unicode"""

        self.start_date = None
        """:type: datetime"""

        self.code = None

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ScheduleMetadata
        """
        schedule_metadata = cls()

        schedule_metadata.modified = parse_datetime(dct.pop("modified"))

        schedule_metadata.md5 = dct.pop("md5")

        schedule_metadata.start_date = parse_date(dct.pop("startDate"))

        # optional
        if "code" in dct:
            schedule_metadata.code = dct.pop("code")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ScheduleMetadata: %s", ", ".join(dct.keys()))

        return schedule_metadata


class Schedule(object):
    def __init__(self):
        self.response_status = None
        """:type: ResponseStatus"""

        self.station_id = None
        """:type: unicode"""

        self.broadcasts = []
        """:type: list[Broadcast]"""

        self.metadata = None
        """:type: ScheduleMetadata"""

    def get_program_ids(self):
        return list({broadcast.program_id for broadcast in self.broadcasts})

    def __unicode__(self):
        return u"{1.start_date} Schedule for Station {0.station_id}".format(self, self.metadata)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @staticmethod
    def from_dict(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Schedule
        """
        if "stationID" not in dct:
            return dct

        schedule = Schedule()

        schedule.response_status = ResponseStatus.from_dict(dct)

        schedule.station_id = dct.pop("stationID")

        schedule.broadcasts = Broadcast.from_iterable(dct.pop("programs"))

        schedule.metadata = ScheduleMetadata.from_dict(dct.pop("metadata"))

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Schedule: %s", ", ".join(dct.keys()))

        return schedule


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


class Broadcast(object):
    def __init__(self):
        self.program_id = None
        """:type: unicode"""

        self.md5 = None
        """:type: unicode"""

        self.air_date_time = None
        """:type: datetime"""

        self.duration = None
        """:type: int"""

        # is this showing Live, or Tape Delayed?. Possible values: "Live", "Tape", "Delay".
        self.live_tape_delay = None
        """:type: unicode"""

        # Values are: "Season Premiere", "Season Finale", "Series Premiere", "Series Finale"
        self.is_premiere_or_finale = None
        """:type: unicode"""

        # is this showing new?
        self.is_new = False
        """:type: bool"""

        self.is_cable_in_the_classroom = False
        """:type: bool"""

        # typically only found outside of North America
        self.is_catchup = False
        """:type: bool"""

        # typically only found outside of North America
        self.is_continued = False
        """:type: bool"""

        self.is_educational = False
        """:type: bool"""

        self.is_joined_in_progress = False
        """:type: bool"""

        self.is_left_in_progress = False
        """:type: bool"""

        # Should only be found in Miniseries and Movie program types.
        self.is_premiere = False
        """:type: bool"""

        # Program stops and will restart later (frequently followed by a continued). Typically only found outside of North America.
        self.is_program_break = False
        """:type: bool"""

        # An encore presentation. Repeat should only be found on a second telecast of sporting events.
        self.is_repeat = False
        """:type: bool"""

        # Program has an on-screen person providing sign-language translation.
        self.is_signed = False
        """:type: bool"""

        self.is_subject_to_blackout = False
        """:type: bool"""

        self.is_time_approximate = False
        """:type: bool"""

        self.audio_properties = []
        """:type: list[unicode]"""

        self.video_properties = []
        """:type: list[unicode]"""

        self.syndication = None

        self.multipart = None
        """:type: MultipartBroadcast"""

        self.ratings = []

        self.parental_advisory = False
        """:type: bool"""

    @property
    def is_live(self):
        """:rtype: bool"""
        if self.live_tape_delay is None:
            return None
        return self.live_tape_delay == u"Live"

    @property
    def is_tape(self):
        """:rtype: bool"""
        if self.live_tape_delay is None:
            return None
        return self.live_tape_delay == u"Tape"

    @property
    def is_delay(self):
        """:rtype: bool"""
        if self.live_tape_delay is None:
            return None
        return self.live_tape_delay == u"Delay"

    @property
    def end_date_time(self):
        """:rtype: datetime"""
        return self.air_date_time + timedelta(seconds=self.duration)

    def __unicode__(self):
        return u"Broadcast of {0.program_id} at {0.air_date_time}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[Broadcast]
        """
        return [cls.from_dict(broadcast) for broadcast in iterable]

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Broadcast
        """
        broadcast = cls()

        broadcast.program_id = dct.pop("programID")

        broadcast.md5 = dct.pop("md5")

        broadcast.air_date_time = parse_datetime(dct.pop("airDateTime"))

        broadcast.duration = dct.pop("duration")

        if "liveTapeDelay" in dct:
            broadcast.live_tape_delay = dct.pop("liveTapeDelay")

        if "isPremiereOrFinale" in dct:
            broadcast.is_premiere_or_finale = dct.pop("isPremiereOrFinale")

        if "new" in dct:
            broadcast.is_new = dct.pop("new")

        if "cableInTheClassroom" in dct:
            broadcast.is_cable_in_the_classroom = dct.pop("cableInTheClassroom")

        if "catchup" in dct:
            broadcast.is_catchup = dct.pop("catchup")

        if "continued" in dct:
            broadcast.is_continued = dct.pop("continued")

        if "educational" in dct:
            broadcast.is_educational = dct.pop("educational")

        if "joinedInProgress" in dct:
            broadcast.is_joined_in_progress = dct.pop("joinedInProgress")

        if "leftInProgress" in dct:
            broadcast.is_left_in_progress = dct.pop("leftInProgress")

        if "premiere" in dct:
            broadcast.is_premiere = dct.pop("premiere")

        if "programBreak" in dct:
            broadcast.is_program_break = dct.pop("programBreak")

        if "repeat" in dct:
            broadcast.is_repeat = dct.pop("repeat")

        if "signed" in dct:
            broadcast.is_signed = dct.pop("signed")

        if "subjectToBlackout" in dct:
            broadcast.is_subject_to_blackout = dct.pop("subjectToBlackout")

        if "timeApproximate" in dct:
            broadcast.is_time_approximate = dct.pop("timeApproximate")

        if "audioProperties" in dct:
            broadcast.audio_properties = dct.pop("audioProperties")

        if "videoProperties" in dct:
            broadcast.video_properties = dct.pop("videoProperties")

        if "syndication" in dct:
            broadcast.syndication = dct.pop("syndication")

        if "multipart" in dct:
            broadcast.multipart = MultipartBroadcast.from_dict(dct.pop("multipart"))

        if "ratings" in dct:
            broadcast.ratings = dct.pop("ratings")

        if "parentalAdvisory" in dct:
            broadcast.parental_advisory = dct.pop("parentalAdvisory")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Broadcast: %s", ", ".join(dct.keys()))

        return broadcast


class Artwork(object):
    def __init__(self):
        self.width = None
        """:type: int"""

        self.height = None
        """:type: int"""

        self.caption = None
        """:type: dict"""

        self.uri = None
        """:type: unicode"""

        self.size = None
        """:type: unicode"""

        self.aspect = None
        """:type: unicode"""

        self.category = None
        """:type: unicode"""

        self.text = None
        """:type: bool"""

        self.primary = None
        """:type: bool"""

        self.tier = None
        """:type: unicode"""

    @property
    def url(self):
        if self.uri[0:7] == u"assets/":
            return u"https://json.schedulesdirect.org/20141201/image/" + self.uri

        return self.uri

    def __unicode__(self):
        return u"{0.tier} {0.category} {0.size} {0.width}x{0.height} ({0.aspect}) {0.url}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Artwork
        """
        artwork = cls()

        if "width" in dct:
            artwork.width = int(dct.pop("width"))

        if "height" in dct:
            artwork.height = int(dct.pop("height"))

        if "caption" in dct:
            artwork.caption = dct.pop("caption")

        if "uri" in dct:
            artwork.uri = dct.pop("uri")

        if "size" in dct:
            artwork.size = dct.pop("size")

        if "aspect" in dct:
            artwork.aspect = dct.pop("aspect")

        if "category" in dct:
            artwork.category = dct.pop("category")

        if "text" in dct:
            artwork.text = (dct.pop("text") == "yes")

        if "primary" in dct:
            artwork.primary = (dct.pop("primary") == "true")

        if "tier" in dct:
            artwork.tier = dct.pop("tier")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Artwork: %s", ", ".join(dct.keys()))

        return artwork

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: list[Artwork]
        """
        return [Artwork.from_dict(item) for item in iterable]


class ArtworkAlbum(list):
    def __init__(self, *args, **kwargs):
        super(ArtworkAlbum, self).__init__(*args, **kwargs)

    def aspect_preference(self, *aspects):
        return ArtworkAlbum(artwork for aspect in aspects for artwork in self if artwork.aspect == aspect)

    def category_preference(self, *categories):
        return ArtworkAlbum(artwork for category in categories for artwork in self if artwork.category == category)

    def size_preference(self, *sizes):
        return ArtworkAlbum(artwork for size in sizes for artwork in self if artwork.size == size)

    def tier_preference(self, *tiers):
        return ArtworkAlbum(artwork for tier in tiers for artwork in self if (tier is None and artwork.tier is None) or artwork.tier == tier)

    @classmethod
    def from_iterable(cls, iterable):
        """

        :param iterable:
        :type iterable: collections.Iterable[dict]
        :return:
        :rtype: ArtworkAlbum
        """
        return cls(Artwork.from_iterable(iterable))


class ProgramArtwork(object):
    def __init__(self):
        self.artwork_id = None
        """:type: unicode"""

        self.artwork_album = ArtworkAlbum()
        """:type: ArtworkAlbum"""

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

        program_artwork.artwork_album = ArtworkAlbum.from_iterable(dct.pop("data"))

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
