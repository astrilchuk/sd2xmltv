import logging
from util import unique


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
