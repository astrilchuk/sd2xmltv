#!/usr/bin/python
# coding=utf-8

from datetime import datetime, timedelta
from dateutil import parser
import logging

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

    @staticmethod
    def decode(dct):
        response_status = ResponseStatus()

        if 'code' in dct:
            response_status.code = dct['code']
            del dct['code']
        else:
            return None

        if 'response' in dct:
            response_status.response = dct['response']
            del dct['response']

        if 'message' in dct:
            response_status.message = dct['message']
            del dct['message']

        if 'serverID' in dct:
            response_status.server_id = dct['serverID']
            del dct['serverID']

        if 'datetime' in dct:
            response_status.date_time = parse_datetime(dct['datetime'])
            del dct['datetime']

        return response_status

class Token(object):
    def __init__(self):
        self.response_status = None
        """:type: ResponseStatus"""

        self.token = None
        """:type: unicode"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Token
        """
        token = Token()

        token.response_status = ResponseStatus.decode(dct)

        if 'token' in dct:
            token.token = dct['token']
            del dct['token']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Token: ' + key)

        return token

class StatusAccount(object):
    def __init__(self):
        self.expires = None
        """:type: datetime"""

        self.messages = None
        """:type: list[unicode]"""

        self.max_lineups = None
        """:type: int"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StatusAccount
        """
        status_account = StatusAccount()

        if 'expires' in dct:
            status_account.expires = parse_datetime(dct['expires'])
            del dct['expires']

        if 'messages' in dct:
            status_account.messages = dct['messages']
            del dct['messages']

        if 'maxLineups' in dct:
            status_account.max_lineups = dct['maxLineups']
            del dct['maxLineups']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for StatusAccount: ' + key)

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

    @staticmethod
    def decode(dct):
        system_status = StatusSystem()

        if 'date' in dct:
            system_status.date = parse_datetime(dct['date'])
            del dct['date']

        if 'details' in dct:
            system_status.details = dct['details']
            del dct['details']

        if 'status' in dct:
            system_status.status = dct['status']
            del dct['status']

        if 'message' in dct:
            system_status.message = dct['message']
            del dct['message']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for StatusSystem: ' + key)

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

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Status
        """
        status = Status()

        if 'account' in dct:
            status.account = StatusAccount.decode(dct['account'])
            del dct['account']

        if 'lineups' in dct:
            for lineup in dct['lineups']:
                status.lineups.append(Lineup.decode(lineup))
            del dct['lineups']

        if 'lastDataUpdate' in dct:
            status.last_data_update = parse_datetime(dct['lastDataUpdate'])
            del dct['lastDataUpdate']

        if 'notifications' in dct:
            status.notifications = dct['notifications']
            del dct['notifications']

        if 'systemStatus' in dct:
            if len(dct['systemStatus']) != 0:
                status.system_status = StatusSystem.decode(dct['systemStatus'][0])
                del dct['systemStatus']

        if 'serverID' in dct:
            status.server_id = dct['serverID']
            del dct['serverID']

        if 'code' in dct:
            status.code = dct['code']
            del dct['code']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Status: ' + key)

        return status

class AddRemoveLineupResponse(object):
    def __init__(self):
        self.response_status = None
        """:type: ResponseStatus"""

        self.changes_remaining = None
        """:type: int"""

    def __str__(self):
        return self.message

    def __unicode__(self):
        return self.message

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :return:
        """
        add_remove_lineup_response = AddRemoveLineupResponse()

        add_remove_lineup_response.response_status = ResponseStatus.decode(dct)

        if 'changesRemaining' in dct:
            add_remove_lineup_response.changes_remaining = dct['changesRemaining']
            del dct['changesRemaining']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for AddLineupResponse: ' + key)

        return add_remove_lineup_response

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

    def __str__(self):
        return self.lineup_id

    def __unicode__(self):
        return self.lineup_id

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :return:
        """
        lineup = Lineup()

        if 'lineup' in dct:
            lineup.lineup_id = dct['lineup']
            del dct['lineup']

        if 'name' in dct:
            lineup.name = dct['name']
            del dct['name']

        if 'transport' in dct:
            lineup.transport = dct['transport']
            del dct['transport']

        if 'location' in dct:
            lineup.location = dct['location']
            del dct['location']

        if 'modified' in dct:
            lineup.modified = parse_datetime(dct['modified'])
            del dct['modified']

        if 'uri' in dct:
            lineup.uri = dct['uri']
            if lineup.lineup_id is None:
                lineup.lineup_id = lineup.uri.split('/')[3]
            del dct['uri']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Lineup: ' + key)

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

    def __str__(self):
        return '{0} / {1} / {2}'.format(self.headend_id, self.transport, self.location)

    def __unicode__(self):
        return '{0} / {1} / {2}'.format(self.headend_id, self.transport, self.location)

    @staticmethod
    def decode(dct):
        """

        :param headend_id:
        :param dct:
        :return:
        """
        headend = Headend()

        if 'headend' in dct:
            headend.headend_id = dct['headend']
            del dct['headend']

        if 'transport' in dct:
            headend.type = dct['transport']
            del dct['transport']

        if 'location' in dct:
            headend.location = dct['location']
            del dct['location']

        if 'lineups' in dct:
            for lineup in dct['lineups']:
                headend.lineups.append(Lineup.decode(lineup))
            del dct['lineups']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Headend: ' + key)

        return headend

class LineupMapping(object):
    def __init__(self):
        self.channels = []
        """:type: list[Channel]"""

        self.stations = []
        """:type: list[Station]"""

        self.metadata = None
        """:type: Lineup"""

    def __str__(self):
        return self.metadata.lineup_id

    def __unicode__(self):
        return self.metadata.lineup_id

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Lineup
        """
        lineup_mapping = LineupMapping()

        if 'stations' in dct:
            for station in dct['stations']:
                lineup_mapping.stations.append(Station.decode(station))
            del dct['stations']

        if 'map' in dct:
            for channel in dct['map']:
                channel = Channel.decode(channel)
                channel.lineup_mapping = lineup_mapping
                lineup_mapping.channels.append(channel)
            del dct['map']

        for channel in lineup_mapping.channels:
            channel.station = lineup_mapping.get_station(channel.station_id)

        if 'metadata' in dct:
            lineup_mapping.lineup = Lineup.decode(dct['metadata'])
            del dct['metadata']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for LineupMapping: ' + key)

        return lineup_mapping

    def get_station(self, station_id):
        """

        :param station_id:
        :type station_id: str
        :return:
        :rtype: Station
        """
        matches = [station for station in self.stations if station.station_id == station_id]
        if len(matches) == 0:
            return None
        return matches[0]

class Channel(object):
    def __init__(self):

        # Common
        self.station_id = None
        """:type: unicode"""

        self.station = None
        """:type: Station"""

        self.channel = None
        """:type: unicode"""

        self.lineup_mapping = None
        """:type: LineupMapping"""

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
        if self.atsc_major is not None:
            yield '%s.%s %s' % (self.atsc_major, self.atsc_minor, self.station.callsign)
            yield '%s.%s' % (self.atsc_major, self.atsc_minor)

        if self.uhf_vhf is not None:
            yield '%s %s fcc' % (self.uhf_vhf, self.station.callsign)

        if self.channel is not None:
            yield '%s %s' % (self.channel, self.station.callsign)
            yield self.channel

        yield self.station.callsign
        yield self.station.name

    # TODO: Xmltv specific, move out of schedulesdirect
    def get_unique_id(self):
        return 'I{0}.{1}.schedulesdirect.org'.format(self.channel, self.station_id)

    def __str__(self):
        return self.get_unique_id()

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Channel
        """
        channel = Channel()

        if 'stationID' in dct:
            channel.station_id = dct['stationID']
            del dct['stationID']

        if 'channel' in dct:
            channel.channel = dct['channel']
            del dct['channel']

        # Antenna

        if 'atscMajor' in dct:
            channel.atsc_major = dct['atscMajor']
            del dct['atscMajor']

        if 'atscMinor' in dct:
            channel.atsc_minor = dct['atscMinor']
            del dct['atscMinor']

        if 'uhfVhf' in dct:
            channel.uhf_vhf = dct['uhfVhf']
            del dct['uhfVhf']

        if channel.channel is None and channel.atsc_major is not None and channel.atsc_minor is not None:
            channel.channel = '{0}.{1}'.format(channel.atsc_major, channel.atsc_minor)

        if channel.channel is None and channel.uhf_vhf is not None:
            channel.channel = str(channel.uhf_vhf)

        # DVB-T/C/S

        if 'frequencyHz' in dct:
            channel.frequency_hz = dct['frequencyHz']
            del dct['frequencyHz']

        if 'deliverySystem' in dct:
            channel.delivery_system = dct['deliverySystem']
            del dct['deliverySystem']

        if 'modulationSystem' in dct:
            channel.modulation_system = dct['modulationSystem']
            del dct['modulationSystem']

        if 'symbolrate' in dct:
            channel.symbol_rate = dct['symbolrate']
            del dct['symbolrate']

        if 'serviceID' in dct:
            channel.service_id = dct['serviceID']
            del dct['serviceID']

        if 'networkID' in dct:
            channel.network_id = dct['networkID']
            del dct['networkID']

        if 'transportID' in dct:
            channel.transport_id = dct['transportID']
            del dct['transportID']

        if 'polarization' in dct:
            channel.polarization = dct['polarization']
            del dct['polarization']

        if 'fec' in dct:
            channel.fec = dct['fec']
            del dct['fec']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Channel: ' + key)

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

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :return:
        """
        broadcaster = Broadcaster()

        if 'city' in dct:
            broadcaster.city = dct['city']
            del dct['city']

        if 'state' in dct:
            broadcaster.state = dct['state']
            del dct['state']

        if 'postalcode' in dct:
            broadcaster.postalcode = dct['postalcode']
            del dct['postalcode']

        if 'country' in dct:
            broadcaster.country = dct['country']
            del dct['country']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Broadcaster: ' + key)

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

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: StationLogo
        """
        station_logo = StationLogo()

        if 'URL' in dct:
            station_logo.url = dct['URL']
            del dct['URL']

        if 'height' in dct:
            station_logo.height = dct['height']
            del dct['height']

        if 'width' in dct:
            station_logo.width = dct['width']
            del dct['width']

        if 'md5' in dct:
            station_logo.md5 = dct['md5']
            del dct['md5']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for StationLogo: ' + key)

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

        self.broadcast_language = []
        """:type: list[unicode]"""

        self.description_language = []
        """:type: list[unicode]"""

        self.broadcaster = None
        """:type: Broadcaster"""

        self.logo = None
        """:type: StationLogo"""

        self.is_commercial_free = False
        """:type: bool"""

        self.affiliate = None
        """:type: unicode"""

        self.schedules = None
        """:type: list[Schedule]"""

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Station
        """
        station = Station()

        if 'stationID' in dct:
            station.station_id = dct['stationID']
            del dct['stationID']

        if 'callsign' in dct:
            station.callsign = dct['callsign']
            del dct['callsign']

        if 'name' in dct:
            station.name = dct['name']
            del dct['name']

        if 'affiliate' in dct:
            station.affiliate = dct['affiliate']
            del dct['affiliate']

        if 'broadcastLanguage' in dct:
            for broadcast_language in dct['broadcastLanguage']:
                station.broadcast_language.append(broadcast_language)
            del dct['broadcastLanguage']

        if 'descriptionLanguage' in dct:
            for description_language in dct['descriptionLanguage']:
                station.description_language.append(description_language)
            del dct['descriptionLanguage']

        if 'broadcaster' in dct:
            station.broadcaster = Broadcaster.decode(dct['broadcaster'])
            del dct['broadcaster']

        if 'logo' in dct:
            station.logo = StationLogo.decode(dct['logo'])
            del dct['logo']

        if 'isCommercialFree' in dct:
            station.is_commercial_free = dct['isCommercialFree']
            del dct['isCommercialFree']

        if 'affiliate' in dct:
            station.affiliate = dct['affiliate']
            del dct['affiliate']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Station: ' + key)

        return station

class ProgramTitles(object):
    def __init__(self):
        self.title120 = None
        """:type: unicode"""

    @staticmethod
    def decode(arr):
        """

        :param arr:
        :return:
        """
        program_titles = ProgramTitles()

        for item in arr:
            if 'title120' in item:
                program_titles.title120 = item['title120']
                del item['title120']
            else:
                logging.warn('Titles not processed: ' + str(item))

        return program_titles

class SeasonEpisode(object):
    def __init__(self):
        self.season = None
        """:type : int"""

        self.episode = None
        """:type : int"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: SeasonEpisode
        """
        season_episode = SeasonEpisode()

        if 'season' in dct:
            season_episode.season = dct['season']
            del dct['season']

        if 'episode' in dct:
            season_episode.episode = dct['episode']
            del dct['episode']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for SeasonEpisode: ' + key)

        return season_episode

class ProgramMetadata(object):
    def __init__(self):
        self.season_episode = None
        """:type : SeasonEpisode"""

    @staticmethod
    def decode(arr):
        """

        :param arr:
        :return:
        """
        program_metadata = ProgramMetadata()
        for item in arr:
            if 'Gracenote' in item:
                program_metadata.season_episode = SeasonEpisode.decode(item['Gracenote'])
                del item['Gracenote']
            else:
                logging.warn('Program metadata not processed: ' + str(item))

        return program_metadata

class ProgramDescription(object):
    def __init__(self):
        self.description = None
        """:type: unicode"""

        self.language = None
        """:type: unicode"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramDescription
        """
        program_description = ProgramDescription()

        if 'description' in dct:
            program_description.description = dct['description']
            del dct['description']

        if 'descriptionLanguage' in dct:
            program_description.language = dct['descriptionLanguage']
            del dct['descriptionLanguage']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for QualityRating: ' + key)

        return program_description

class ProgramDescriptions(object):
    def __init__(self):
        self.description100 = []
        """:type: list[ProgramDescription]"""

        self.description1000 = []
        """:type: list[ProgramDescription]"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramDescriptions
        """
        program_descriptions = ProgramDescriptions()

        if 'description100' in dct:
            for description in dct['description100']:
                program_descriptions.description100.append(ProgramDescription.decode(description))
            del dct['description100']

        if 'description1000' in dct:
            for description in dct['description1000']:
                program_descriptions.description1000.append(ProgramDescription.decode(description))
            del dct['description1000']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramDescriptions: ' + key)

        return program_descriptions

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
        stars_str = unichr(0x2606) * rating_int
        if rating_float - rating_int > 0:
            stars_str += unichr(0x00BD)
        return stars_str

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: QualityRating
        """
        quality_rating = QualityRating()

        if 'increment' in dct:
            quality_rating.increment = dct['increment']
            del dct['increment']

        if 'maxRating' in dct:
            quality_rating.max_rating = dct['maxRating']
            del dct['maxRating']

        if 'minRating' in dct:
            quality_rating.min_rating = dct['minRating']
            del dct['minRating']

        if 'rating' in dct:
            quality_rating.rating = dct['rating']
            del dct['rating']

        if 'ratingsBody' in dct:
            quality_rating.ratings_body = dct['ratingsBody']
            del dct['ratingsBody']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for QualityRating: ' + key)

        return quality_rating

class ProgramMovie(object):
    def __init__(self):
        self.duration = None
        """:type: int"""

        self.quality_ratings = []
        """:type: list[QualityRating]"""

        self.year = None
        """:type: unicode"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramMovie
        """
        program_movie = ProgramMovie()

        if 'duration' in dct:
            program_movie.duration = dct['duration']
            del dct['duration']

        if 'qualityRating' in dct:
            for quality_rating in dct['qualityRating']:
                program_movie.quality_ratings.append(QualityRating.decode(quality_rating))
            del dct['qualityRating']

        if 'year' in dct:
            program_movie.year = dct['year']
            del dct['year']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramMovie: ' + key)

        return program_movie

class ProgramContentRating(object):
    def __init__(self):
        self.body = None
        """:type: unicode"""

        self.code = None
        """:type: unicode"""

    def __str__(self):
        return u'{0}: {1}'.format(self.body, self.code)

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramContentRating
        """
        program_content_rating = ProgramContentRating()

        if 'body' in dct:
            program_content_rating.body = dct['body']
            del dct['body']

        if 'code' in dct:
            program_content_rating.code = dct['code']
            del dct['code']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramContentRating: ' + key)

        return program_content_rating

class ProgramRecommendation(object):
    def __init__(self):
        self.program_id = None
        """:type: unicode"""

        self.title120 = None
        """:type: unicode"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ProgramRecommendation
        """
        program_recommendation = ProgramRecommendation()

        if 'programID' in dct:
            program_recommendation.program_id = dct['programID']
            del dct['programID']

        if 'title120' in dct:
            program_recommendation.title120 = dct['title120']
            del dct['title120']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramRecommendation: ' + key)

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
        return unicode(self).encode('utf-8')

    @staticmethod
    def decode(dct):
        program_cast = ProgramCast()

        if 'personId' in dct:
            program_cast.person_id = dct['personId']
            del dct['personId']

        if 'nameId' in dct:
            program_cast.name_id = dct['nameId']
            del dct['nameId']

        if 'billingOrder' in dct:
            program_cast.billing_order = dct['billingOrder']
            del dct['billingOrder']

        if 'role' in dct:
            program_cast.role = dct['role']
            del dct['role']

        if 'name' in dct:
            program_cast.name = dct['name']
            del dct['name']

        if 'characterName' in dct:
            program_cast.character_name = dct['characterName']
            del dct['characterName']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramCast: ' + key)

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
        return unicode(self).encode('utf-8')

    @staticmethod
    def decode(dct):
        program_crew = ProgramCrew()

        if 'personId' in dct:
            program_crew.person_id = dct['personId']
            del dct['personId']

        if 'nameId' in dct:
            program_crew.name_id = dct['nameId']
            del dct['nameId']

        if 'billingOrder' in dct:
            program_crew.billing_order = dct['billingOrder']
            del dct['billingOrder']

        if 'role' in dct:
            program_crew.role = dct['role']
            del dct['role']

        if 'name' in dct:
            program_crew.name = dct['name']
            del dct['name']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramCrew: ' + key)

        return program_crew

class EventTeam(object):
    def __init__(self):
        self.name = None
        """:type: unicode"""

        self.is_home = False
        """:type: bool"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :return:
        """
        event_team = EventTeam()

        if 'name' in dct:
            event_team.name = dct['name']
            del dct['name']

        if 'isHome' in dct:
            event_team.is_home = dct['isHome']
            del dct['isHome']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramEventDetails: ' + key)

        return event_team

class ProgramEventDetails(object):
    def __init__(self):
        self.venue = None
        """:type: unicode"""

        self.game_date = None
        """:type: datetime"""

        self.teams = []
        """:type: list[EventTeam]"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :return:
        """
        ped = ProgramEventDetails()

        if 'venue100' in dct:
            ped.venue = dct['venue100']
            del dct['venue100']

        if 'gameDate' in dct:
            ped.game_date = parser.parse(dct['gameDate'])
            del dct['gameDate']

        if 'teams' in dct:
            for team in dct['teams']:
                ped.teams.append(EventTeam.decode(team))
            del dct['teams']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ProgramEventDetails: ' + key)

        return ped

class Program(object):
    def __init__(self):
        self.program_id = None
        """:type: unicode"""

        self.titles = ProgramTitles()
        """:type: ProgramTitles"""

        self.event_details = None
        """:type: ProgramEventDetails"""

        self.descriptions = ProgramDescriptions()
        """:type: ProgramDescriptions"""

        self.original_air_date = None
        """:type: date"""

        self.genres = []
        """:type: list[unicode]"""

        self.episode_title = None
        """:type: unicode"""

        self.metadata = ProgramMetadata()
        """:type: ProgramMetadata"""

        self.cast = []
        """:type: list[ProgramCast]"""

        self.crew = []
        """:type: list[ProgramCrew]"""

        self.show_type = None
        """:type: unicode"""

        self.has_image_artwork = None
        """:type: bool"""

        self.md5 = None
        """:type: unicode"""

        self.content_ratings = []
        """:type: list[ProgramContentRatings]"""

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
        """:type: unicode"""

        self.official_url = None
        """:type: unicode"""

    def __str__(self):
        return u'{0} "{1}"'.format(self.program_id, self.titles.title120)

    def get_content_rating(self, body):
        content_ratings = [content_rating for content_rating in self.content_ratings if content_rating.body == body]
        if len(content_ratings) != 0:
            return content_ratings[0].code
        return None

    def get_mpaa_content_rating(self):
        return self.get_content_rating(u'Motion Picture Association of America')

    def get_cast(self, in_roles):
        return [cast for cast in self.cast if cast.role in in_roles]

    def get_crew(self, in_roles):
        return [crew for crew in self.crew if crew.role in in_roles]

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Program
        """
        program = Program()

        if 'programID' in dct:
            program.program_id = dct['programID']
            if program.program_id[:2] == 'EP':
                program.episode_num = int(program.program_id[-4:])
            del dct['programID']

        if 'titles' in dct:
            program.titles = ProgramTitles.decode(dct['titles'])
            del dct['titles']

        if 'md5' in dct:
            program.md5 = dct['md5']
            del dct['md5']

        if 'eventDetails' in dct:
            program.event_details = ProgramEventDetails.decode(dct['eventDetails'])
            del dct['eventDetails']

        if 'descriptions' in dct:
            program.descriptions = ProgramDescriptions.decode(dct['descriptions'])
            del dct['descriptions']

        if 'originalAirDate' in dct:
            program.original_air_date = parse_date(dct['originalAirDate'])
            del dct['originalAirDate']

        if 'genres' in dct:
            program.genres = dct['genres']
            del dct['genres']

        if 'episodeTitle150' in dct:
            program.episode_title = dct['episodeTitle150']
            del dct['episodeTitle150']

        if 'metadata' in dct:
            program.metadata = ProgramMetadata.decode(dct['metadata'])
            del dct['metadata']

        if 'cast' in dct:
            for cast in dct['cast']:
                program.cast.append(ProgramCast.decode(cast))
            del dct['cast']

        if 'crew' in dct:
            for crew in dct['crew']:
                program.cast.append(ProgramCast.decode(crew))
            del dct['crew']

        if 'showType' in dct:
            program.show_type = dct['showType']
            del dct['showType']

        if 'hasImageArtwork' in dct:
            program.has_image_artwork = dct['hasImageArtwork']
            del dct['hasImageArtwork']

        if 'contentRating' in dct:
            for content_rating in dct['contentRating']:
                program.content_ratings.append(ProgramContentRating.decode(content_rating))
            del dct['contentRating']

        if 'contentAdvisory' in dct:
            program.content_advisories = dct['contentAdvisory']
            del dct['contentAdvisory']

        if 'recommendations' in dct:
            for recommendation in dct['recommendations']:
                program.recommendations.append(ProgramRecommendation.decode(recommendation))
            del dct['recommendations']

        if 'movie' in dct:
            program.movie = ProgramMovie.decode(dct['movie'])
            del dct['movie']

        if 'animation' in dct:
            program.animation = dct['animation']
            del dct['animation']

        if 'audience' in dct:
            program.audience = dct['audience']
            del dct['audience']

        if 'holiday' in dct:
            program.holiday = dct['holiday']
            del dct['holiday']

        if 'keyWords' in dct:
            program.keywords = dct['keyWords']
            del dct['keyWords']

        if 'officialURL' in dct:
            program.official_url = dct['officialURL']
            del dct['officialURL']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Program: ' + key)

        return program

class ScheduleMetadata(object):
    def __init__(self):
        self.modified = None
        """:type: datetime"""

        self.md5 = None
        """:type: unicode"""

        self.start_date = None
        """:type: datetime"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: ScheduleMetadata
        """
        schedule_metadata = ScheduleMetadata()

        if 'modified' in dct:
            schedule_metadata.modified = parse_datetime(dct['modified'])
            del dct['modified']

        if 'md5' in dct:
            schedule_metadata.md5 = dct['md5']
            del dct['md5']

        if 'startDate' in dct:
            schedule_metadata.start_date = parse_date(dct['startDate'])
            del dct['startDate']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for ScheduleMetadata: ' + key)

        return schedule_metadata

class Schedule(object):
    def __init__(self):
        self.response_status = None
        """:type: ResponseStatus"""

        self.station_id = None
        """:type: unicode"""

        self.station = None
        """:type: Station"""

        self.airings = []
        """:type: list[Airing]"""

        self.metadata = None
        """:type: ScheduleMetadata"""

    def __str__(self):
        return 'Schedule for {0}'.format(self.metadata.start_date)

    def __unicode__(self):
        return 'Schedule for {0}'.format(self.metadata.start_date)

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Schedule
        """
        schedule = Schedule()

        schedule.response_status = ResponseStatus.decode(dct)

        if 'stationID' in dct:
            schedule.station_id = dct['stationID']
            del dct['stationID']

        if 'programs' in dct:
            for program in dct['programs']:
                airing = Airing.decode(program)
                airing.schedule = schedule
                schedule.airings.append(airing)
            del dct['programs']

        if 'metadata' in dct:
            schedule.metadata = ScheduleMetadata.decode(dct['metadata'])
            del dct['metadata']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Schedule: ' + key)

        return schedule

class MultipartAiring(object):
    def __init__(self):
        self.part_number = None
        """:type: int"""

        self.total_parts = None
        """:type: int"""

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: MultipartAiring
        """
        multipart_airing = MultipartAiring()

        if 'partNumber' in dct:
            multipart_airing.part_number = dct['partNumber']
            del dct['partNumber']

        if 'totalParts' in dct:
            multipart_airing.total_parts = dct['totalParts']
            del dct['totalParts']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for MultipartAiring: ' + key)

        return multipart_airing

class Airing(object):
    def __init__(self):
        self.schedule = None
        """:type: Schedule"""

        self.program_id = None
        """:type: unicode"""

        self.md5 = None
        """:type: unicode"""

        self.air_date_time = None
        """:type: datetime"""

        self.duration = None
        """:type: int"""

        self.end_date_time = None
        """:type: datetime"""

        # is this showing Live, or Tape Delayed?. Possible values: "Live", "Tape", "Delay".
        self.live_tape_delay = None
        self.is_live = None
        """:type: bool"""

        self.is_tape = None
        """:type: bool"""

        self.is_delay = None
        """:type: bool"""

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
        self.video_properties = []
        self.syndication = None

        self.multipart = None
        """:type: MultipartAiring"""

        self.ratings = []

        self.parental_advisory = False

    @staticmethod
    def decode(dct):
        """

        :param dct:
        :type dct: dict
        :return:
        :rtype: Airing
        """
        airing = Airing()

        if 'programID' in dct:
            airing.program_id = dct['programID']
            del dct['programID']

        if 'md5' in dct:
            airing.md5 = dct['md5']
            del dct['md5']

        if 'airDateTime' in dct:
            airing.air_date_time = parse_datetime(dct['airDateTime'])
            del dct['airDateTime']

        if 'duration' in dct:
            airing.duration = dct['duration']
            del dct['duration']

        if airing.air_date_time is not None and airing.duration is not None:
            airing.end_date_time = airing.air_date_time + timedelta(seconds=airing.duration)

        if 'liveTapeDelay' in dct:
            airing.live_tape_delay = dct['liveTapeDelay']
            airing.is_live = airing.live_tape_delay == "Live"
            airing.is_tape = airing.live_tape_delay == "Tape"
            airing.is_delay = airing.live_tape_delay == "Delay"
            del dct['liveTapeDelay']

        if 'isPremiereOrFinale' in dct:
            airing.is_premiere_or_finale = dct['isPremiereOrFinale']
            del dct['isPremiereOrFinale']

        if 'new' in dct:
            airing.is_new = dct['new']
            del dct['new']

        if 'cableInTheClassroom' in dct:
            airing.is_cable_in_the_classroom = dct['cableInTheClassroom']
            del dct['cableInTheClassroom']

        if 'catchup' in dct:
            airing.is_catchup = dct['catchup']
            del dct['catchup']

        if 'continued' in dct:
            airing.is_continued = dct['continued']
            del dct['continued']

        if 'educational' in dct:
            airing.is_educational = dct['educational']
            del dct['educational']

        if 'joinedInProgress' in dct:
            airing.is_joined_in_progress = dct['joinedInProgress']
            del dct['joinedInProgress']

        if 'leftInProgress' in dct:
            airing.is_left_in_progress = dct['leftInProgress']
            del dct['leftInProgress']

        if 'premiere' in dct:
            airing.is_premiere = dct['premiere']
            del dct['premiere']

        if 'programBreak' in dct:
            airing.is_program_break = dct['programBreak']
            del dct['programBreak']

        if 'repeat' in dct:
            airing.is_repeat = dct['repeat']
            del dct['repeat']

        if 'signed' in dct:
            airing.is_signed = dct['signed']
            del dct['signed']

        if 'subjectToBlackout' in dct:
            airing.is_subject_to_blackout = dct['subjectToBlackout']
            del dct['subjectToBlackout']

        if 'timeApproximate' in dct:
            airing.is_time_approximate = dct['timeApproximate']
            del dct['timeApproximate']

        if 'audioProperties' in dct:
            airing.audio_properties = dct['audioProperties']
            del dct['audioProperties']

        if 'videoProperties' in dct:
            airing.video_properties = dct['videoProperties']
            del dct['videoProperties']

        if 'syndication' in dct:
            airing.syndication = dct['syndication']
            del dct['syndication']

        if 'multipart' in dct:
            airing.multipart = MultipartAiring.decode(dct['multipart'])
            del dct['multipart']

        if 'ratings' in dct:
            airing.ratings = dct['ratings']
            del dct['ratings']

        if 'parentalAdvisory' in dct:
            airing.parental_advisory = dct['parentalAdvisory']
            del dct['parentalAdvisory']

        if len(dct) != 0:
            for key in dct.keys():
                logging.warn('Key not processed for Airing: ' + key)

        return airing

def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()
