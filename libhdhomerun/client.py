import urllib2
from common import Lineup, DiscoveredDeviceList, DiscoveredDevice, Device
import json
import logging


class HDHomeRunClient(object):
    def __init__(self, ip_list=[]):
        self._logger = logging.getLogger(__name__)

        self._public_discovery_url = "http://ipv4.my.hdhomerun.com/discover"  # type: unicode

        self._local_discovery_url = "http://%s/discover.json"  # type: unicode

        self._local_lineup_url = "http://%s/lineup.json"  # type: unicode

        self._discovered_device_list = None  # type: List[DiscoveredDevice]

        self._device_list = None  # type: List[Device]

        self._ip_list = []  # type: List[unicode]

        if ip_list is unicode:
            self._ip_list = [ip_list]
        else:
            self._ip_list = ip_list

    def init_device_list(self):
        if self._device_list is not None:
            return self._device_list

        self._device_list = []

        if len(self._ip_list) == 0:
            if self._discovered_device_list is None:
                self._logger.info("Discovering devices via my.hdhomerun.com...")
                self._discovered_device_list = self.discover_devices()

            if len(self._discovered_device_list) == 0:
                self._logger.error("No devices reported by my.hdhomerun.com.")
                return False
            else:
                self._logger.info("my.hdhomerun.com reports {0} device(s) on your network.".format(len(self._discovered_device_list)))

            for discovered_device in self._discovered_device_list:
                self._logger.info("Getting info for device {0.device_id} at {0.local_ip}...".format(discovered_device))
                device = self.get_device_from_discovered_device(discovered_device)
                if device is None:
                    self._logger.error("Could not get info for device at {0.local_ip}.".format(discovered_device))
                else:
                    self._logger.info("Found device \"{0.friendly_name} {0.model_number}\" ({0.device_id}) running firmware version {0.firmware_version} at {0.base_url}.".format(device))
                    self._device_list.append(device)
        else:
            for ip in self._ip_list:
                self._logger.info("Getting info for device at {0}...".format(ip))
                device = self.get_device_from_ip(ip)
                if device is None:
                    self._logger.error("Could not get info for device at {0}.".format(ip))
                else:
                    self._logger.info("Found device \"{0.friendly_name} {0.model_number}\" ({0.device_id}) running firmware version {0.firmware_version} at {0.base_url}.".format(device))
                    self._device_list.append(device)

        return True

    def init_hdhomerun_lineups(self):
        for device in self._device_list:
            lineup = self.get_lineup_from_device(device)
            device.lineup = lineup

    def get_channel_list(self):
        channel_list = set()
        for device in self._device_list:
            for channel in device.lineup:
                channel_list.add(channel.guide_number)
        return channel_list

    def get_lineup_from_discovered_device(self, discovered_device):  # type: (DiscoveredDevice) -> Lineup
        """

        :param discovered_device:
        :return:
        """
        return self.get_lineup_from_lineup_url(discovered_device.lineup_url)

    def get_lineup_from_device(self, device):  # type: (Device) -> Lineup
        """

        :param device:
        :return:
        """
        return self.get_lineup_from_lineup_url(device.lineup_url)

    def get_lineup_from_ip(self, ip):  # type: (unicode) -> Lineup
        """

        :param ip:
        :return:
        """
        return self.get_lineup_from_lineup_url(self._local_lineup_url % (ip,))

    def get_lineup_from_lineup_url(self, url):  # type: (unicode) -> Lineup
        """

        :param url:
        :return:
        """
        response = urllib2.urlopen(url)

        encoding = response.headers['content-type'].split('charset=')[-1]

        json_text = unicode(response.read(), encoding=encoding)

        return Lineup.from_iterable(json.loads(json_text))

    def get_device_from_ip(self, ip):  # type: (unicode) -> Device
        """

        :param ip:
        :return:
        """
        return self.get_device_from_url(self._local_discovery_url % (ip,))

    def get_device_from_discovered_device(self, discovered_device):  # type: (DiscoveredDevice) -> Device
        """

        :param device:
        :return:
        """
        return self.get_device_from_url(discovered_device.discover_url)

    def get_device_from_url(self, url):  # type: (unicode) -> Device
        """

        :param url:
        :return:
        """
        response = urllib2.urlopen(url)

        encoding = response.headers['content-type'].split('charset=')[-1]

        json_text = unicode(response.read(), encoding)

        return Device.from_dict(json.loads(json_text))

    def discover_devices(self):  # type: () -> DiscoveredDeviceList
        """

        :return:
        """
        response = urllib2.urlopen(self._public_discovery_url)

        encoding = response.headers['content-type'].split('charset=')[-1]

        json_text = unicode(response.read(), encoding)

        return DiscoveredDeviceList.from_iterable(json.loads(json_text))
