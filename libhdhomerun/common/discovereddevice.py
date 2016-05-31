

class DiscoveredDevice(object):
    def __init__(self):
        self.device_id = None  # type: unicode

        self.local_ip = None  # type: unicode

        self.base_url = None  # type: unicode

        self.discover_url = None  # type: unicode

        self.lineup_url = None  # type: unicode

    def __unicode__(self):  # type: () -> unicode
        return "Device {0.device_id} at {0.local_ip}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> DiscoveredDevice
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
