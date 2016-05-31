import logging
import collections

class Image(object):
    def __init__(self):
        self.width = None  # type: int

        self.height = None  # type: int

        self.caption = None  # type: dict

        self.uri = None  # type: unicode

        self.size = None  # type: unicode

        self.aspect = None  # type: unicode

        self.category = None  # type: unicode

        self.text = None  # type: bool

        self.primary = None  # type: bool

        self.tier = None  # type: unicode

    @property
    def url(self):  # type: () -> unicode
        if self.uri[0:7] == u"assets/":
            return u"https://json.schedulesdirect.org/20141201/image/" + self.uri

        return self.uri

    def __unicode__(self):  # type: () -> unicode
        return u"{0.tier} {0.category} {0.size} {0.width}x{0.height} ({0.aspect}) {0.url}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Image
        """

        :param dct:
        :return:
        """
        image = cls()

        if "width" in dct:
            image.width = int(dct.pop("width"))

        if "height" in dct:
            image.height = int(dct.pop("height"))

        if "caption" in dct:
            image.caption = dct.pop("caption")

        if "uri" in dct:
            image.uri = dct.pop("uri")

        if "size" in dct:
            image.size = dct.pop("size")

        if "aspect" in dct:
            image.aspect = dct.pop("aspect")

        if "category" in dct:
            image.category = dct.pop("category")

        if "text" in dct:
            image.text = (dct.pop("text") == "yes")

        if "primary" in dct:
            image.primary = (dct.pop("primary") == "true")

        if "tier" in dct:
            image.tier = dct.pop("tier")

        if len(dct) != 0:
            logging.warn("Key(s) not processed for Image: %s", ", ".join(dct.keys()))

        return image

    @classmethod
    def from_iterable(cls, iterable):  # type: (Iterable[dict]) -> List[Image]
        """

        :param iterable:
        :return:
        """
        return [Image.from_dict(item) for item in iterable]
