from discovereddevice import DiscoveredDevice


class DiscoveredDeviceList(list):
    def __init__(self, *args, **kwargs):
        super(DiscoveredDeviceList, self).__init__(*args, **kwargs)

    @classmethod
    def from_iterable(cls, iterable):
        return cls([DiscoveredDevice.from_dict(device) for device in iterable])
