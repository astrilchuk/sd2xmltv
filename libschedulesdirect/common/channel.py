import logging
from station import Station


class Channel(object):
    def __init__(self):
        # Common
        self.station_id = None  # type: unicode

        self.station = None  # type: Station

        self.channel = None  # type: unicode

        # Antenna
        self.atsc_major = None  # type: int

        self.atsc_minor = None  # type: int

        self.uhf_vhf = None  # type: int

        # DVB-T/C/S

        self.frequency_hz = None  # type: int

        self.delivery_system = None  # type: unicode

        self.modulation_system = None  # type: unicode

        self.symbol_rate = None  # type: int

        self.service_id = None  # type: int

        self.network_id = None  # type: int

        self.transport_id = None  # type: int

        self.polarization = None  # type: unicode

        self.fec = None  # type: unicode

    def get_display_names(self):
        if self.channel is not None:
            yield u"{0.channel} {1.callsign}".format(self, self.station)
            yield self.channel

        if self.uhf_vhf is not None:
            yield u"{0.uhf_vhf} {1.callsign} fcc".format(self, self.station)

        yield self.station.callsign
        yield self.station.name

    def get_unique_id(self):  # type: () -> unicode
        return u"I{0.channel}.{0.station_id}.schedulesdirect.org".format(self)

    def __unicode__(self):  # type: () -> unicode
        return u"Channel {0.channel}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[Channel]
        """

        :param iterable:
        :return:
        """
        return [cls.from_dict(channel) for channel in iterable]

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Channel
        """

        :param dct:
        :return:
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
