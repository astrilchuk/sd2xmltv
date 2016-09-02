import logging
from collections import Iterable
from datetime import datetime, timedelta
from util import parse_datetime
from multipartbroadcast import MultipartBroadcast


class Broadcast(object):
    def __init__(self):
        self.program_id = None  # type: unicode

        self.md5 = None  # type: unicode

        self.air_date_time = None  # type: datetime

        self.duration = None  # type: int

        # is this showing Live, or Tape Delayed?. Possible values: "Live", "Tape", "Delay".
        self.live_tape_delay = None  # type: unicode

        # Values are: "Season Premiere", "Season Finale", "Series Premiere", "Series Finale"
        self.is_premiere_or_finale = None  # type: unicode

        # is this showing new?
        self.is_new = False  # type: bool

        self.is_cable_in_the_classroom = False  # type: bool

        # typically only found outside of North America
        self.is_catchup = False  # type: bool

        # typically only found outside of North America
        self.is_continued = False  # type: bool

        self.is_educational = False  # type: bool

        self.is_joined_in_progress = False  # type: bool

        self.is_left_in_progress = False  # type: bool

        # Should only be found in Miniseries and Movie program types.
        self.is_premiere = False  # type: bool

        # Program stops and will restart later (frequently followed by a continued).
        # Typically only found outside of North America.
        self.is_program_break = False  # type: bool

        # An encore presentation. Repeat should only be found on a second telecast of sporting events.
        self.is_repeat = False  # type: bool

        # Program has an on-screen person providing sign-language translation.
        self.is_signed = False  # type: bool

        self.is_subject_to_blackout = False  # type: bool

        self.is_time_approximate = False  # type: bool

        self.audio_properties = []  # type: List[unicode]

        self.video_properties = []  # type: List[unicode]

        self.multipart = None  # type: MultipartBroadcast

        self.parental_advisory = False  # type: bool

    @property
    def is_live(self):  # type: () -> bool
        if self.live_tape_delay is None:
            return None
        return self.live_tape_delay == u"Live"

    @property
    def is_tape(self):  # type: () -> bool
        if self.live_tape_delay is None:
            return None
        return self.live_tape_delay == u"Tape"

    @property
    def is_delay(self):  # type: () -> bool
        if self.live_tape_delay is None:
            return None
        return self.live_tape_delay == u"Delay"

    @property
    def end_date_time(self):  # type: () -> datetime
        return self.air_date_time + timedelta(seconds=self.duration)

    def __unicode__(self):  # type: () -> unicode
        return u"Broadcast of {0.program_id} at {0.air_date_time}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[Broadcast]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(broadcast) for broadcast in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Broadcast
        """

        :param dct:
        :return:
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

        if "multipart" in dct:
            broadcast.multipart = MultipartBroadcast.from_dict(dct.pop("multipart"))

        # ratings in Broadcast is deprecated so just pop if found
        if "ratings" in dct:
            dct.pop("ratings")

        if "parentalAdvisory" in dct:
            broadcast.parental_advisory = dct.pop("parentalAdvisory")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Broadcast: %s", ", ".join(dct.keys()))

        return broadcast
