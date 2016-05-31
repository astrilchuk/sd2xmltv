import logging
from datetime import date
from util import unique
from schedule import Schedule


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
        # note: curly braces create a set
        return list({(broadcast.program_id, broadcast.md5) for schedule in self for broadcast in schedule.broadcasts})

    def get_program_max_schedule_dates(self):
        return [(program_id, max_schedule_date) for program_id, max_schedule_date in {broadcast.program_id: schedule.metadata.start_date for schedule in self.order_by_start_date() for broadcast in schedule.broadcasts}.iteritems()]

    def filter_station(self, station_id):
        return ScheduleList(schedule for schedule in self if schedule.station_id == station_id)

    def filter_schedule_date(self, schedule_date):
        return ScheduleList(schedule for schedule in self if schedule.schedule_date == schedule_date)

    def get_schedule(self, station_id, schedule_date):  # type: (unicode, date) -> Schedule
        """

        :param station_id:
        :param schedule_date:
        :return:
        """
        return next((schedule for schedule in self if schedule.station_id == station_id and schedule.metadata.start_date == schedule_date), None)

    @staticmethod
    def from_iterable(iterable):  # type: (Iterable[dict]) -> ScheduleList
        return ScheduleList([Schedule.from_dict(item) for item in iterable])
