# coding=utf-8

import ConfigParser
import io
from libhdhomerun.client import HDHomeRunClient
import os.path


class MetaChannelFilter(object):
    def __init__(self):
        self._channel_filters = []

    def add_channel_filter(self, channel_filter):
        self._channel_filters.append(channel_filter)

    def pass_channel(self, lineup, channel):
        for channel_filter in self._channel_filters:
            if not channel_filter.pass_channel(lineup, channel):
                return False

        return True


class FileChannelFilter(object):
    def __init__(self, config_path, lineup_map_list):
        self._config = ConfigParser.ConfigParser(allow_no_value=True)
        self._config.optionxform = str
        self._dirty = False
        self._load_config(config_path)
        self._apply_lineup_map_list(lineup_map_list)
        self._save_config(config_path)

    def _apply_lineup_map_list(self, lineup_map_list):
        config_changed = False

        for lineup_map in lineup_map_list:
            config_section = lineup_map.lineup.lineup_id
            config_section_new = config_section + "-new"
            config_section_include = config_section + u"-include"
            config_section_exclude = config_section + u"-exclude"

            if not self._config.has_section(config_section_new):
                config_changed = True
                self._config.add_section(config_section_new)
                self._config.set(config_section_new, "action", "include")
            else:
                if not self._config.has_option(config_section_new, "action") or self._config.get(config_section_new, "action") not in ["include", "exclude"]:
                    config_changed = True
                    self._config.set(config_section_new, "action", "include")

            if not self._config.has_section(config_section_include):
                config_changed = True
                self._config.add_section(config_section_include)

            if not self._config.has_section(config_section_exclude):
                config_changed = True
                self._config.add_section(config_section_exclude)

            for channel in lineup_map.channels:
                channel_option = channel.channel + u"_" + channel.station.station_id
                channel_option_value = channel.station.name.encode('utf-8')

                if not self._config.has_option(config_section_new, channel_option) and \
                        not self._config.has_option(config_section_include, channel_option) and \
                        not self._config.has_option(config_section_exclude, channel_option):
                    config_changed = True
                    self._config.set(config_section_new, channel_option, channel_option_value)

        if config_changed:
            self._dirty = True

    def _load_config(self, config_path):
        if os.path.isfile(config_path):
            with io.open(config_path, 'r', encoding='utf-8') as fp:
                self._config.readfp(fp)

        self._dirty = False

    def _save_config(self, config_path, force_save=False):
        if not self._dirty and not force_save:
            return

        with open(config_path, "wb") as fp:
            fp.write("; sd2xmltv channel filter\n")
            fp.write("; \n")
            fp.write("; Move channels to include under [<headend>-include].\n")
            fp.write("; Move channels to exclude under [<headend>-exclude].\n")
            fp.write("; Newly found channels appear under [<headend>-new].\n")
            fp.write("; Modify 'action = [include|exclude]' to specify how new channels should be handled.\n")
            fp.write("; Note: New channels are not automatically moved from the [<headend>-new] section.\n")
            fp.write("; Cut and paste newly found channels under [<headend>-include] or [<headend>-exclude].\n")
            fp.write("\n")
            self._config.write(fp)

        self._dirty = False

    def pass_channel(self, lineup, channel):
        config_section_new = lineup.lineup_id + "-new"
        config_section_include = lineup.lineup_id + "-include"
        channel_option = channel.channel + "_" + channel.station.station_id
        result = self._config.has_option(config_section_include, channel_option) or \
                 (self._config.has_option(config_section_new, channel_option) and not self._config.get(config_section_new, "action") == "exclude")
        return result


class HdhomerunChannelFilter(object):
    def __init__(self, hdhomerun_ip="discover"):
        if hdhomerun_ip == "discover":
            client = HDHomeRunClient()
        else:
            client = HDHomeRunClient(hdhomerun_ip.split(","))

        client.init_device_list()

        client.init_hdhomerun_lineups()

        self._channels = client.get_channel_list()

    def pass_channel(self, lineup, channel):
        return channel.channel in self._channels
