import logging
from responsestatus import ResponseStatus
from broadcast import Broadcast
from schedulemetadata import ScheduleMetadata


class Schedule(object):
    def __init__(self):
        self.response_status = None  # type: ResponseStatus

        self.station_id = None  # type: unicode

        self.broadcasts = []  # type: List[Broadcast]

        self.metadata = None  # type: ScheduleMetadata

    def get_program_ids(self):  # type: () -> List[unicode]
        return list({broadcast.program_id for broadcast in self.broadcasts})

    def __unicode__(self):  # type: () -> unicode
        return u"{1.start_date} Schedule for Station {0.station_id}".format(self, self.metadata)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @staticmethod
    def from_dict(dct):  # type: (dict) -> Schedule
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
