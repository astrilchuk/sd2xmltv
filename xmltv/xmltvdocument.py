import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from . import indent


class XmltvDocument(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.root = Element(u"tv")

    def add_channel(self, xmltv_channel):
        self.root.append(xmltv_channel.root)

    def add_programme(self, xmltv_programme):
        self.root.append(xmltv_programme.root)

    def has_channel(self, channel_id):
        return self.root.find("./channel[@channel=\"{0}\"]".format(channel_id)) is not None

    def save(self, path, encoding=u"utf-8"):
        indent(self.root)
        ET.ElementTree(self.root).write(path, encoding=encoding, xml_declaration=True)
