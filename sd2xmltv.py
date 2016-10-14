#!/usr/bin/python
# coding=utf-8

import argparse
import logging
import logging.config
from xmltv import XmltvChannel, XmltvProgramme, XmltvWriter
from libschedulesdirect.common import Status, Program, Broadcast, Channel, ProgramArtwork
from libschedulesdirect.schedulesdirect import SchedulesDirect
from datetime import datetime
from libhdhomerun.client import HDHomeRunClient
from itertools import islice


class Sd2Xmltv:
    def __init__(self, options):
        self._logger = logging.getLogger("sd2xmltv")  # type: logging.Logger

        self._encoding = u"utf-8"  # type: unicode

        self._sd = SchedulesDirect(options.username, options.password)  # type: SchedulesDirect

        self._status = None  # type: Status

        self._output_path = options.output_path  # type: unicode

        self._days = options.days  # type: int

        self._hdhomerun_ip = options.hdhomerun  # type: unicode

        self._episode_title_in_description = False  # type: bool

        self._content_rating_preference_order = \
            [u"Motion Picture Association of America", u"USA Parental Rating", u"Canadian Parental Rating"]
        # type: List[unicode]

    def login(self):
        self._logger.info(u"Getting SchedulesDirect token.")
        self._sd.get_token()

        self._logger.info(u"Getting SchedulesDirect status.")
        self._status = self._sd.get_status()

        if not self._sd.is_online():
            raise Exception(u"System is not online.")

        expiry_delta = self._status.account.expires - datetime.utcnow()
        expiry_days = int(expiry_delta.total_seconds() // 86400)
        if expiry_days > 14:
            self._logger.info(u"Account will expire on %s (%s days).", self._status.account.expires, expiry_days)
        else:
            self._logger.warn(u"Account will expire on %s (%s days).", self._status.account.expires, expiry_days)

        time_delta = datetime.utcnow() - self._status.last_data_update
        hours, minutes = int(time_delta.total_seconds() // 3600), int((time_delta.total_seconds() % 3600) // 60)
        self._logger.info(u"SchedulesDirect last update at %s (%s hours %s minutes ago).", self._status.last_data_update, hours, minutes)

        if self._status.system_status.message is not None:
            self._logger.info(u"Message: %s", self._status.system_status.message)

    def manage(self):
        self._sd.manage()

    def process(self):
        if len(self._status.lineups) == 0:
            self._logger.info(u"Not subscribed to any lineups, exiting.")
            return

        channel_filter = None

        if self._hdhomerun_ip is not None:
            if self._hdhomerun_ip == "discover":
                client = HDHomeRunClient()
            else:
                client = HDHomeRunClient(self._hdhomerun_ip.split(","))

            client.init_device_list()

            client.init_hdhomerun_lineups()

            channel_filter = client.get_channel_list()

        self._logger.info(u"Getting station/channel mappings for %s lineups.", len(self._status.lineups))
        lineup_map_list = self._sd.get_lineup_map_list(self._status.lineups)

        # self._filter = self.read_filter(lineup_map_list)
        
        station_ids = [station.station_id for station in lineup_map_list.unique_stations(channel_filter)]

        self._logger.info(u"Getting schedule hashes...")
        schedule_hash_list = self._sd.get_schedule_hash_list(station_ids)

        self._sd.refresh_cache(schedule_hash_list)

        with XmltvWriter(self._output_path) as f:

            f.write(u"<?xml version=\"1.0\" encoding=\"{0}\" ?>\n".format(self._encoding).encode(self._encoding))
            f.write(u"<tv>\n".encode(self._encoding))

            self._logger.info(u"Adding channels to xmltv document...")
            for channel in lineup_map_list.unique_channels(channel_filter):
                self._add_channel(f, channel)

            self._logger.info(u"Adding programs to xmltv document...")
            total_programs_added = 0
            for channel in lineup_map_list.unique_channels(channel_filter):

                channel_programs_added = 0

                schedule_list = self._sd.get_cached_schedules([(channel.station_id, None)])
                program_lookup = self._sd.get_cached_programs(schedule_list.get_program_ids())

                artwork_ids = {program.artwork_id for program in program_lookup.values() if program.has_image_artwork}
                program_artwork_lookup = self._sd.get_cached_artwork(list(artwork_ids))

                for date in islice(schedule_list.schedule_dates(), self._days):
                    programs_added = 0

                    schedule = schedule_list.get_schedule(channel.station_id, date)
                    if schedule is None:
                        continue

                    # check for error statuses from SD - for example 7020 SCHEDULE RANGE EXCEEDED
                    # TODO: better handling of error responses
                    if schedule.response_status is not None and schedule.response_status.code != 0:
                        self._logger.warn(u"Skipping day due to: %s", schedule.response_status.message)
                        continue

                    for broadcast in schedule.broadcasts:
                        programs_added += 1
                        program = program_lookup[broadcast.program_id]
                        program_artwork = program_artwork_lookup.get(program.artwork_id, None)
                        self._add_programme(f, program, channel, broadcast, program_artwork)

                    self._logger.debug(u"Added %s programs for channel %s on %s.", programs_added, channel.get_display_names().next(), date)

                    channel_programs_added += programs_added

                self._logger.info(u"Added %s programs for channel %s.", channel_programs_added, channel.get_display_names().next())

                total_programs_added += channel_programs_added

            self._logger.info(u"Added %s total programs.", total_programs_added)

            f.write(u"</tv>\n".encode(self._encoding))

        self._logger.info(u"Finished.")

    def _get_program_categories(self, program):  # type: (Program) -> Set[unicode]
        """

        :param program:
        :return:
        """
        categories = set()

        if program.is_sports_entity:
            categories.add(u"Sports")

        elif program.is_movie_entity:
            categories.add(u"Movie / Drama")

        elif program.is_show_entity or program.is_episode_entity:
            if u"Children" in program.genres:
                categories.add(u"Children's / Youth programs")

            if u"Educational" in program.genres:
                categories.add(u"Education / Science / Factual topics")

            if u"Science" in program.genres:
                categories.add(u"Education / Science / Factual topics")

            if u"Newsmagazine" in program.genres:
                categories.add(u"News magazine")

            if u"Documentary" in program.genres:
                categories.add(u"Documentary")

            if u"News" in program.genres:
                categories.add(u"News / Current affairs")

            if u"Music" in program.genres:
                categories.add(u"Music / Ballet / Dance")

        else:
            self._logger.warn(u"Unknown entity type: %s", program.entity_type)

        return categories

    def _add_programme(self, fp, program, channel, broadcast, program_artwork):
        """

        :param fp:
        :param program:
        :type program: Program
        :param channel:
        :type channel: Channel
        :param broadcast:
        :type broadcast: Broadcast
        :param program_artwork:
        :type program_artwork: ProgramArtwork
        :return:
        """
        p = XmltvProgramme(broadcast.air_date_time, broadcast.end_date_time, channel.get_unique_id())

        p.add_title(program.titles.title120)

        if program.episode_title is not None:
            p.add_subtitle(program.episode_title)

        for category in self._get_program_categories(program):
            p.add_category(category)

        # for genre in program.genres:
        #    p.add_category("sd: " + genre)

        p.add_episode_num_dd_progid(program.program_id)

        if program.is_episode_entity:
            if program.metadata is not None and \
                            program.metadata.season_episode is not None and \
                            program.metadata.season_episode.has_season_episode:
                if broadcast.multipart is None:
                    p.add_episode_num_xmltv_ns(
                        season_num=program.metadata.season_episode.season,
                        episode_num=program.metadata.season_episode.episode)
                else:
                    p.add_episode_num_xmltv_ns(
                        season_num=program.metadata.season_episode.season,
                        episode_num=program.metadata.season_episode.episode,
                        part_num=broadcast.multipart.part_number,
                        total_parts=broadcast.multipart.total_parts)
            elif program.episode_num is not None:
                if broadcast.multipart is not None:
                    p.add_episode_num_xmltv_ns(
                        part_num=broadcast.multipart.part_number,
                        total_parts=broadcast.multipart.total_parts)
                p.add_episode_num_onscreen(u"E{0}".format(program.episode_num))

        if program.descriptions is None:
            self._add_programme_description(broadcast, p, program, None)
        else:
            for description_language in program.descriptions.languages():
                self._add_programme_description(broadcast, p, program, description_language)

        if program.movie is not None:
            for quality_rating in program.movie.quality_ratings:
                p.add_star_rating(quality_rating.rating, quality_rating.max_rating, quality_rating.ratings_body)

        if program.is_episode_entity and not broadcast.is_new and program.original_air_date is not None:
            p.add_previously_shown(start=program.original_air_date)

        if program_artwork is not None:
            # "Banner-L2", "Banner-L3", "Iconic", "Staple"
            image_list = program_artwork.image_list.aspect_preference(u"3x4", u"4x3", u"2x3", u"16x9").size_preference(u"Md").category_preference(u"Poster Art", u"Box Art", u"Banner", u"Banner-L1", u"Banner-LO", u"Banner-L2", u"Logo").tier_preference(u"Series", u"Season", u"Sport", u"Team", u"Organization", u"College", None)
            image = image_list[0] if image_list else None
            if image is not None:
                p.add_icon(image.url)

        p.save(fp, encoding=self._encoding)

    def _add_programme_description(self, broadcast, p, program, description_language):
        description_elements = []

        if self._episode_title_in_description and program.episode_title is not None:
            description_elements.append(u"\"{0}\"".format(program.episode_title))

        program_attributes = []

        if program.show_type is not None:
            program_attributes.append(program.show_type)

        if program.movie is not None and program.movie.year is not None:
            program_attributes.append(program.movie.year)
        elif broadcast.is_live:
            program_attributes.append(u"Live")
        elif broadcast.is_new:
            program_attributes.append(u"New")
        elif program.original_air_date is not None:
            program_attributes.append(unicode(program.original_air_date.strftime("%Y-%m-%d")))

        if program.is_episode_entity:
            if program.metadata is not None and \
                            program.metadata.season_episode is not None and \
                            program.metadata.season_episode.has_season_episode:
                program_attributes.append(u"S{0.season}E{0.episode}".format(program.metadata.season_episode))
            elif program.episode_num is not None:
                program_attributes.append(u"E{0}".format(program.episode_num))

        if broadcast.multipart is not None:
            program_attributes.append(u"{0.part_number} of {0.total_parts}".format(broadcast.multipart))

        if len(program.content_ratings) != 0:
            for preference in self._content_rating_preference_order:
                rating = program.get_content_rating(preference)
                if rating is None:
                    continue
                program_attributes.append(rating.code)
                break

        if program.movie is not None and len(program.movie.quality_ratings) != 0:
            selected_quality_rating = next((quality_rating for quality_rating in program.movie.quality_ratings if quality_rating.max_rating == u"4"), None)
            if selected_quality_rating is not None:
                program_attributes.append(selected_quality_rating.get_stars())

        if len(program_attributes) != 0:
            description_elements.append(u"; ".join(program_attributes))

        if description_language is not None:
            longest_text = program.descriptions.get_longest_text(language=description_language)
            description_elements.append(longest_text)

        if len(program.recommendations) != 0:
            description_elements.append(u"See also: {0}".format(u", ".join([pr.title120 for pr in program.recommendations])))

        p.add_description(u" \u2022 ".join(description_elements), lang=description_language)

    def _add_channel(self, fp, channel):
        channel_id = channel.get_unique_id()

        self._logger.info(u"Adding channel %s to xmltv document.", channel_id)
        xmltv_channel = XmltvChannel(channel_id)
        [xmltv_channel.add_display_name(display_name) for display_name in channel.get_display_names()]

        xmltv_channel.save(fp, encoding=self._encoding)

    def _export_icons(self, stations):
        import urllib
        import os
        from urlparse import urlparse
        for station in stations:
            if station.logo is None:
                continue
            url = station.logo.url
            path = urlparse(url)
            (path, filename) = os.path.split(path[2])
            (filename, extension) = os.path.splitext(filename)

            image_on_web = urllib.urlopen(url)
            if image_on_web.headers.maintype != "image":
                image_on_web.close()
                continue
            f = open(station.station_id + extension, "wb")
            f.write(image_on_web.read())
            f.close()
            image_on_web.close()


def main():
    parser = argparse.ArgumentParser(prog=u"sd2xmltv.py", description=u"A Schedules Direct to xmltv converter.", add_help=False)

    required_args = parser.add_argument_group(u"required arguments")
    required_args.add_argument(u"-u", u"--username", dest=u"username", help=u"SchedulesDirect.org username.", required=True)
    required_args.add_argument(u"-p", u"--password", dest=u"password", help=u"SchedulesDirect.org password.", required=True)

    optional_args = parser.add_argument_group(u"optional arguments")
    optional_args.add_argument(u"-h", u"--help", action=u"help")
    optional_args.add_argument(u"-v", u"--version", action=u"version", version=u"sd2xmltv 0.2.1")
    optional_args.add_argument(u"-o", u"--output", dest=u"output_path", default=u"./xmltv.xml", help=u"Output path and filename (use .gz to compress).")
    optional_args.add_argument(u"-d", u"--days", dest=u"days", type=int, default=14, help=u"Number of days to import")
    optional_args.add_argument(u"-m", u"--manage", dest=u"manage", action="store_true", default=False, help=u"Manage lineups")
    optional_args.add_argument(u"--hdhomerun", dest=u"hdhomerun", default=None, help=u"HDHomeRun IP address or 'discover' for channel filtering.")

    args = parser.parse_args()

    app = Sd2Xmltv(args)
    app.login()

    if args.manage:
        app.manage()
    else:
        app.process()

if __name__ == "__main__":
    logging.config.fileConfig(u"logging.cfg", disable_existing_loggers=True)
    main()
