import logging
from util import parse_date
from schedulehash import ScheduleHash


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
    def from_dict(cls, dct):  # type: (dict) -> ScheduleHashList
        """

        :param dct:
        :return:
        """
        return cls([ScheduleHash.from_dict(dct[station_id][schedule_date], station_id, parse_date(schedule_date)) for station_id in dct for schedule_date in dct[station_id]])
