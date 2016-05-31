import logging
from servicecountry import ServiceCountry


class ServiceRegion(object):
    def __init__(self):
        self.name = None  # type: unicode

        self.service_countries = []  # type: List[ServiceCountry]

    @classmethod
    def from_dict(cls, name, dct):
        """

        :param dct:
        :return:
        """

        service_region = cls()

        service_region.name = name

        service_region.service_countries = ServiceCountry.from_iterable()
