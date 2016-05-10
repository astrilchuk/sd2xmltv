
class Lineup(list):
    def __init__(self, *args, **kwargs):
        super(Lineup, self).__init__(*args, **kwargs)

    def get_channel_numbers(self):
        return [channel.guide_number for channel in self]

    @classmethod
    def from_iterable(cls, iterable):
        return cls([Channel.from_dict(dct) for dct in iterable])


class Channel(object):
    def __init__(self):
        self.guide_number = None
        """:type: unicode"""

        self.guide_name = None
        """:type: unicode"""

        self.url = None
        """:type: unicode"""

        self.is_hd = False
        """:type: bool"""

        self.is_favorite = False
        """:type: bool"""

    def __unicode__(self):
        return "{0.guide_number} {0.guide_name}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        channel = cls()

        if "GuideNumber" in dct:
            channel.guide_number = dct.pop("GuideNumber")

        if "GuideName" in dct:
            channel.guide_name = dct.pop("GuideName")

        if "URL" in dct:
            channel.url = dct.pop("URL")

        if "HD" in dct:
            if dct.pop("HD") == 1:
                channel.is_hd = True

        if "Favorite" in dct:
            if dct.pop("Favorite") == 1:
                channel.is_favorite = True

        return channel


class DiscoveredDeviceList(list):
    def __init__(self, *args, **kwargs):
        super(DiscoveredDeviceList, self).__init__(*args, **kwargs)

    @classmethod
    def from_iterable(cls, iterable):
        return cls([DiscoveredDevice.from_dict(device) for device in iterable])


class DiscoveredDevice(object):
    def __init__(self):
        self.device_id = None
        """:type: unicode"""

        self.local_ip = None
        """:type: unicode"""

        self.base_url = None
        """:type: unicode"""

        self.discover_url = None
        """:type: unicode"""

        self.lineup_url = None
        """:type: unicode"""

    def __unicode__(self):
        return "Device {0.device_id} at {0.local_ip}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        discovered_device = cls()

        if "DeviceID" in dct:
            discovered_device.device_id = dct.pop("DeviceID")

        if "LocalIP" in dct:
            discovered_device.local_ip = dct.pop("LocalIP")

        if "BaseURL" in dct:
            discovered_device.base_url = dct.pop("BaseURL")

        if "DiscoverURL" in dct:
            discovered_device.discover_url = dct.pop("DiscoverURL")

        if "LineupURL" in dct:
            discovered_device.lineup_url = dct.pop("LineupURL")

        return discovered_device


class Device(object):
    def __init__(self):
        self.friendly_name = None
        """:type: unicode"""

        self.model_number = None
        """:type: unicode"""

        self.firmware_name = None
        """:type: unicode"""

        self.firmware_version = None
        """:type: unicode"""

        self.device_id = None
        """:type: unicode"""

        self.device_auth = None
        """:type: unicode"""

        self.base_url = None
        """:type: unicode"""

        self.lineup_url = None
        """:type: unicode"""

        self.lineup = None
        """:type: Lineup"""

    def __unicode__(self):
        return "Device {0.device_id} at {0.base_url}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):
        device = cls()

        if "FriendlyName" in dct:
            device.friendly_name = dct.pop("FriendlyName")

        if "ModelNumber" in dct:
            device.model_number = dct.pop("ModelNumber")

        if "FirmwareName" in dct:
            device.firmware_name = dct.pop("FirmwareName")

        if "FirmwareVersion" in dct:
            device.firmware_version = dct.pop("FirmwareVersion")

        if "DeviceID" in dct:
            device.device_id = dct.pop("DeviceID")

        if "DeviceAuth" in dct:
            device.device_auth = dct.pop("DeviceAuth")

        if "BaseURL" in dct:
            device.base_url = dct.pop("BaseURL")

        if "LineupURL" in dct:
            device.lineup_url = dct.pop("LineupURL")

        return device
