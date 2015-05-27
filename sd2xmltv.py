#!/usr/bin/python
# coding=utf-8

import logging
from xmltv.common import XmltvDocument, XmltvChannel, XmltvProgramme
from libschedulesdirect.common import Status, Program, Airing, Channel
from libschedulesdirect.schedulesdirect import SchedulesDirect
from optparse import OptionParser
import datetime
from datetime import timedelta
import gzip

class Sd2Xmltv:

    def __init__(self, options):
        self._sd = SchedulesDirect(options.username, options.password)
        self._status = None

        self._logger = logging.getLogger(__name__)
        self._xmltv_document = XmltvDocument()
        self._output_path = options.output_path
        self._days = options.days

        self._callsign_whitelist = None
        self._callsign_blacklist = None

        self._content_rating_preference_order = [u'Motion Picture Association of America', u'USA Parental Rating', u'Canadian Parental Rating']

        self._include_credits = False
        self._include_see_also = False

        self._genres = set()

    def login(self):
        self._logger.info('Getting SchedulesDirect token.')
        self._sd.get_token()

        self._logger.info('Getting SchedulesDirect status.')
        self._status = Status.decode(self._sd.get_status())

        if not self._sd.is_online():
            raise Exception('System is not online.')

        expiry_delta = self._status.account.expires - datetime.datetime.utcnow()
        self._logger.info('Account will expire on {0} ({1} days).'.format(self._status.account.expires, int(expiry_delta.total_seconds() // 86400)))

        time_delta = datetime.datetime.utcnow() - self._status.last_data_update
        hours, minutes = int(time_delta.total_seconds() // 3600), int((time_delta.total_seconds() % 3600) // 60)
        self._logger.info('SchedulesDirect last update at {0} ({1} hours {2} minutes ago).'.format(self._status.last_data_update, hours, minutes))

        if self._status.system_status.message is not None:
            self._logger.info('Message: {0}'.format(self._status.system_status.message))

    def process(self):

        if len(self._status.lineups) == 0:
            self._logger.info('Not subscribed to any lineups, exiting.')
            return

        self._logger.info('Getting station/channel mappings for {0} lineups.'.format(len(self._status.lineups)))
        lineup_mappings = self._sd.get_lineup_mappings([(lineup.lineup_id, lineup.modified) for lineup in self._status.lineups])

        #self._callsign_whitelist = ['CBLTDT', 'CHCHDT', 'CKCODT', 'CICADT', 'CHCJDT', 'CJMTDT', 'CIIID41', 'CFMTDT', 'CITYDT']

        station_ids = {channel.station.station_id for channel in self._enumerate_channels(lineup_mappings)}

        current_date = datetime.datetime.utcnow().date()

        schedule_dates = [(current_date + timedelta(days = x)).strftime('%Y-%m-%d') for x in range(0, self._days)]

        self._logger.info('Getting schedules for {0} stations.'.format(len(station_ids)))
        schedules = self._sd.get_schedules(station_ids, schedule_dates)

        for channel in self._enumerate_channels(lineup_mappings):
            channel.station.schedules = [schedule for schedule in schedules if channel.station.station_id == schedule.station_id]

        self._logger.info('Caching new or changed programs...')
        programs = [(airing.program_id, airing.md5) for airing in self._enumerate_airings(lineup_mappings)]
        self._sd.cache_programs(programs)

        self._logger.info('Adding channels to xmltv document...')
        for channel in self._enumerate_channels(lineup_mappings):
            self._add_channel(channel)

        self._logger.info('Adding programs to xmltv document...')
        total_programs_added = 0
        for channel in self._enumerate_channels(lineup_mappings):
            programs_added = 0
            for schedule in channel.station.schedules:
                self._logger.info('Adding programs on %s for channel %s.' %
                                  (schedule.metadata.start_date.strftime("%Y-%m-%d"),
                                  channel.get_display_names().next()))
                for airing in schedule.airings:
                    programs_added += 1
                    self._add_programme(channel, airing)
            self._logger.info('Added %s programs for channel %s.' %
                              (programs_added, channel.get_display_names().next()))
            total_programs_added += programs_added
        self._logger.info('Added %s total programs.' % total_programs_added)


        self._logger.info('Saving ' + self._output_path)

        if self._output_path[-2:] == 'gz':
            f = gzip.open(self._output_path, 'wb')
            self._xmltv_document.save(f)
            f.close()
        else:
            self._xmltv_document.save(self._output_path)

        return

    def manage(self):
        while True:
            print('\nManage Account Options:\n')
            print('1. List subscribed lineups')
            print('2. Add lineup')
            print('3. Remove lineup')
            print('4. List lineup channels.')
            print('\nChoose an option or \'x\' to exit.')
            choice = raw_input('> ')
            if choice == 'x':
                break
            if choice == '1':
                self._list_subscribed_lineups()
            elif choice == '2':
                self._add_lineup()
            elif choice == '3':
                self._remove_lineup()
            elif choice == '4':
                self._list_lineup_channels()

    def _list_subscribed_lineups(self):
        lineups = self._sd.get_subscribed_lineups()
        print '\nSubscribed Lineups:\n'
        for lineup in lineups:
            print 'Lineup:\t%s' % lineup.lineup_id
            print 'Name:\t%s' % lineup.name
            print 'Transport:\t%s' % lineup.transport
            print 'Location:\t%s' % lineup.location
            print ''

    def _add_lineup(self):
        while True:
            print '\nAdd Lineup\n'
            print 'Enter 5-digit zip or postal code or \'x\' to cancel:'
            postal_code = raw_input('> ')
            if postal_code == 'x':
                break

            country = 'USA'
            if postal_code[0].isalpha():
                country = 'CAN'

            headends = self._sd.get_headends_by_postal_code(country, postal_code)

            while True:
                subscribed_lineups = self._sd.get_subscribed_lineups()
                subscribed_lineup_ids = [lineup.lineup_id for lineup in subscribed_lineups]

                headend_lineups = [(headend, lineup) for headend in headends for lineup in headend.lineups if lineup.lineup_id not in subscribed_lineup_ids]

                transport_set = set()

                for (headend, lineup) in headend_lineups:
                    transport_set.add(headend.type)

                options = []
                count = 0
                for transport in transport_set:
                    print '\nTransport: %s\n' % transport
                    for (headend, lineup) in [(headend, lineup) for (headend, lineup) in headend_lineups if headend.type == transport]:
                        options.append((headend, lineup))
                        count += 1
                        print '\t%s. %s (%s)' % (count, lineup.name, headend.location)

                print '\nChoose a lineup to add or \'x\' to cancel.'
                choice = raw_input('> ')

                if choice == 'x':
                    break

                choice = int(choice) - 1
                (headend, lineup) = options[choice]

                print 'Are you sure you want to add \'%s (%s)\'? (y/n)' % (lineup.name, headend.location)
                if raw_input('> ') != 'y':
                    continue

                response = self._sd.add_lineup(lineup.lineup_id)

                print 'Schedules Direct returned \'%s\'.' % response.message
                print '%s lineup changes remaining.\n' % response.changes_remaining

    def _list_lineup_channels(self):

        while True:
            print '\nList Lineup Channels\n'

            subscribed_lineups = self._sd.get_subscribed_lineups()

            options = []
            count = 0
            for lineup in subscribed_lineups:
                count += 1
                options.append(lineup)
                print '%s. %s (%s)' % (count, lineup.name, lineup.location)

            print '\nChoose a lineup to list channels or \'x\' to cancel.'
            choice = raw_input('> ')
            if choice == 'x':
                break

            choice = int(choice) - 1
            lineup = options[choice]

            lineup_mapping = self._sd.get_lineup_mapping(lineup.lineup_id)

            for channel in lineup_mapping.channels:
                print '%s\t%s.%s\t%s\t%s "%s"' % (channel.uhf_vhf, channel.atsc_major, channel.atsc_minor, channel.channel, channel.station.callsign, channel.station.name)

            #print 'Are you sure you want to remove \'%s (%s)\'? (y/n)' % (lineup.name, lineup.location)
            #if raw_input('> ') != 'y':
            #    continue

    def _remove_lineup(self):

        while True:
            print '\nRemove Lineup\n'

            subscribed_lineups = self._sd.get_subscribed_lineups()

            options = []
            count = 0
            for lineup in subscribed_lineups:
                count += 1
                options.append(lineup)
                print '%s. %s (%s)' % (count, lineup.name, lineup.location)

            print '\nChoose a lineup to remove or \'x\' to cancel.'
            choice = raw_input('> ')
            if choice == 'x':
                break

            choice = int(choice) - 1
            lineup = options[choice]

            print 'Are you sure you want to remove \'%s (%s)\'? (y/n)' % (lineup.name, lineup.location)
            if raw_input('> ') != 'y':
                continue

            response = self._sd.remove_lineup(lineup.lineup_id)

            print '\nSchedules Direct returned \'%s\'.' % response.message
            print '%s lineup changes remaining.\n' % response.changes_remaining

    def _enumerate_channels(self, lineups):
        result = [channel for lineup in lineups for channel in lineup.channels]

        if self._callsign_whitelist is not None:
            result = [channel for channel in result if channel.station.callsign in self._callsign_whitelist]

        if self._callsign_blacklist is not None:
            result = [channel for channel in result if channel.station.callsign not in self._callsign_blacklist]

        yielded_channels = set()

        for channel in result:
            unique_id = channel.get_unique_id()
            if unique_id in yielded_channels:
                continue
            yield channel
            yielded_channels.add(unique_id)

    def _enumerate_airings(self, lineups):
        for channel in self._enumerate_channels(lineups):
            for schedule in channel.station.schedules:
                for airing in schedule.airings:
                    yield airing

    def _add_program_categories(self, programme, channel, airing, program):
        """

        :param programme:
        :type programme: XmltvProgramme
        :param channel:
        :type channel: Channel
        :param airing:
        :type airing: Airing
        :param program:
        :type program: Program
        :return:
        """
        categories = set()

        if program.program_id[:2] == 'SP':
            categories.add('Sports')

        elif program.program_id[:2] == 'MV':
            categories.add('Movie / Drama')

        elif program.program_id[:2] == 'SH' or program.program_id[:2] == 'EP':
            if 'Children' in program.genres:
                categories.add("Children's / Youth programmes")

            if 'Educational' in program.genres:
                categories.add('Education / Science / Factual topics')

            if 'Science' in program.genres:
                categories.add('Education / Science / Factual topics')

            if 'Newsmagazine' in program.genres:
                categories.add('News magazine')

            if 'Documentary' in program.genres:
                categories.add('Documentary')

            if 'News' in program.genres:
                categories.add('News / Current affairs')

            if 'Music' in program.genres:
                categories.add('Music / Ballet / Dance')

        for category in categories:
            programme.add_category(category)

    def _add_programme(self, channel, airing):
        """

        :param channel:
        :type channel: Channel
        :param airing:
        :type airing: Airing
        :return:
        """

        program = self._sd.get_program(airing.program_id, airing.md5)

        if program is None:
            self._logger.warning('Program id {0} with md5 {1} was not found in cache, trying again with only id.'.format(airing.program_id, airing.md5))
            program = self._sd.get_program(airing.program_id)
            if program is None:
                self._logger.error('Program id {0} not found in cache, skipping adding program.'.format(airing.program_id))
                return
            self._logger.warning('Found Program id {0} \'{1}\' with md5 {2} in cache.'.format(program.program_id, program.titles.title120, program.md5))

        start_time = airing.air_date_time
        stop_time = airing.end_date_time
        channel_id = channel.get_unique_id()

        p = self._xmltv_document.add_programme(start_time, stop_time, channel_id)

        p.add_title(program.titles.title120)

        if program.episode_title is not None:
            p.add_subtitle(program.episode_title)

        self._add_program_categories(p, channel, airing, program)

        #for genre in program.genres:
        #    p.add_category('sd: ' + genre)

        sub_type = None
        if program.event_details is not None:
            if 'subType' in program.event_details:
                sub_type = program.event_details['subType']

        # was airing.is_new
        #if program.program_id[:2] == 'EP' or program.program_id[:2] == 'MV' or program.program_id[:2] == 'SP':
        # tvheadend now supports series subscription filtering so add to all shows
        p.add_episode_num_dd_progid(program.program_id)

        if program.metadata.season_episode is not None:
            if airing.multipart is None:
                p.add_episode_num_xmltv_ns(
                    season_num = program.metadata.season_episode.season,
                    episode_num = program.metadata.season_episode.episode)
            else:
                p.add_episode_num_xmltv_ns(
                    season_num = program.metadata.season_episode.season,
                    episode_num = program.metadata.season_episode.episode,
                    part_num = airing.multipart.part_number,
                    total_parts = airing.multipart.total_parts)
        elif program.episode_num is not None:
            p.add_episode_num_onscreen('E' + str(program.episode_num))

        description_prefix = ''
        if program.episode_title is not None:
            description_prefix = '"' + program.episode_title + '" '

        program_attributes = []

        if sub_type is not None:
            program_attributes.append(sub_type)

        if program.movie is not None and program.movie.year is not None:
            program_attributes.append(program.movie.year)
        elif airing.is_live == True:
            program_attributes.append('Live')
        elif airing.is_new == True:
            program_attributes.append('New')
        elif program.original_air_date is not None:
            program_attributes.append(program.original_air_date.strftime('%Y-%m-%d'))

        if program.metadata.season_episode is not None:
            program_attributes.append('S%sE%s' % (program.metadata.season_episode.season, program.metadata.season_episode.episode))
        elif program.episode_num is not None:
            program_attributes.append('E' + str(program.episode_num))

        if airing.multipart is not None:
            program_attributes.append('%s of %s' % (airing.multipart.part_number, airing.multipart.total_parts))

        if len(program.content_ratings) != 0 and len(self._content_rating_preference_order) != 0:
            for preference in self._content_rating_preference_order:
                rating = program.get_content_rating(preference)
                if rating is None:
                    continue
                program_attributes.append(rating)
                break

        if len(program_attributes) != 0:
            description_prefix = description_prefix + '(' + '; '.join(program_attributes) + ') '

        see_also = ''
        if len(program.recommendations) != 0:
            see_also = ' See also: ' + ', '.join([pr.title120 for pr in program.recommendations])

        if len(program.descriptions.description1000) != 0:
            for description in program.descriptions.description1000:
                p.add_description(description_prefix + description.description + see_also, description.language)
        elif len(program.descriptions.description100) != 0:
            for description in program.descriptions.description100:
                p.add_description(description_prefix + description.description + see_also, description.language)
        else:
            if description_prefix != '':
                p.add_description(description_prefix.strip() + see_also)

        if program.movie is not None:
            for quality_rating in program.movie.quality_ratings:
                p.add_star_rating(quality_rating.rating, quality_rating.max_rating, quality_rating.ratings_body)

        if self._include_credits == False:
            return

        for cast in program.cast:
            if cast['role'] in ['Actor', 'Guest', 'Guest Star', 'Judge', 'Voice', 'Guest Voice', 'Host', 'Narrator', 'Anchor', 'Contestant', 'Correspondent', 'Musical Guest']:
                continue
            self._logger.info('cast: ' + cast['role'])
        actors = program.get_cast(['Actor'])
        guests = program.get_cast(['Guest'])
        guest_stars = program.get_cast(['Guest Star'])
        judges = program.get_cast(['Judge'])
        voices = program.get_cast(['Voice'])
        guest_voices = program.get_cast(['Guest Voice'])
        cast_hosts = program.get_cast(['Host'])
        narrators = program.get_cast(['Narrator'])
        anchors = program.get_cast(['Anchor'])
        contestants = program.get_cast(['Contestant'])
        correspondents = program.get_cast(['Correspondent'])
        musical_guests = program.get_cast(['Musical Guest'])

        for actor in actors:
            p.add_credit_actor(actor.name)

        for guest_star in guest_stars:
            p.add_credit_guest(guest_star)

        directors = program.get_crew(['Director'])
        writers = program.get_crew(['Writer'])
        producers = program.get_crew(['Producer'])

        for director in directors:
            p.add_credit_director(director)

        for writer in writers:
            p.add_credit_writer(writer)

        for producer in producers:
            p.add_credit_producer(producer)

    def _add_channel(self, channel):
        channel_id = channel.get_unique_id()

        if self._xmltv_document.has_channel(channel_id):
            self._logger.info('Skipping channel %s, already added.' % (channel_id))
            return

        self._logger.info('Adding channel %s to xmltv document.' % (channel_id))
        xmltv_channel = self._xmltv_document.add_channel(channel_id)
        [xmltv_channel.add_display_name(display_name) for display_name in channel.get_display_names()]

def main():
    parser = OptionParser()
    parser.add_option('-u', '--username', dest='username', help='SchedulesDirect.org username.')
    parser.add_option('-p', '--password', dest='password', help='SchedulesDirect.org password.')
    parser.add_option('-o', '--output', dest='output_path', default='./xmltv.xml', help='Output path and filename.')
    parser.add_option('-d', '--days', dest='days', type='int', default=14, help='Number of days to import')
    parser.add_option('-m', '--manage', dest='manage', action='store_true', default=False, help='Manage lineups')

    (options, args) = parser.parse_args()

    app = Sd2Xmltv(options)
    app.login()

    if (options.manage == True):
        app.manage()
    else:
        app.process()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
    main()