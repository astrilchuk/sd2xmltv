

class Device(object):
    def __init__(self):
        self.friendly_name = None  # type: unicode

        self.model_number = None  # type: unicode

        self.firmware_name = None  # type: unicode

        self.firmware_version = None  # type: unicode

        self.device_id = None  # type: unicode

        self.device_auth = None  # type: unicode

        self.base_url = None  # type: unicode

        self.lineup_url = None  # type: unicode

        self.lineup = None  # type: Lineup

    def __unicode__(self):  # type: () -> unicode
        return "Device {0.device_id} at {0.base_url}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Device
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
