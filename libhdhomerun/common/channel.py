

class Channel(object):
    def __init__(self):
        self.guide_number = None  # type: unicode

        self.guide_name = None  # type: unicode

        self.url = None  # type: unicode

        self.is_hd = False  # type: bool

        self.is_favorite = False  # type: bool

    def __unicode__(self):  # type: () -> unicode
        return "{0.guide_number} {0.guide_name}".format(self)

    def __str__(self):
        return unicode(self).encode("utf-8")

    @classmethod
    def from_dict(cls, dct):  # type: (dict) -> Channel
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
