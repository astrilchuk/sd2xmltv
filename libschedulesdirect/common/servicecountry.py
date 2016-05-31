import logging


class ServiceCountry(object):
    def __init__(self):
        self.full_name = None  # type: unicode

        self.short_name = None  # type: unicode

        self.postal_code_example = None  # type: unicode

        self.postal_code_regex = None  # type: unicode

        self.one_postal_code = False  # type: bool

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> ServiceCountry
        """

        :param dct:
        :return:
        """
        service_country = cls()

        if "fullName" in dct:
            service_country.full_name = dct.pop("fullName")

        if "shortName" in dct:
            service_country.short_name = dct.pop("shortName")

        if "postalCodeExample" in dct:
            service_country.postal_code_example = dct.pop("postalCodeExample")

        if "postalCode" in dct:
            service_country.postal_code_regex = dct.pop("postalCode")

        if "onePostalCode" in dct:
            service_country.onePostalCode = dct.pop("onePostalCode")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for ServiceCountry: %s", ", ".join(dct.keys()))

        return service_country
