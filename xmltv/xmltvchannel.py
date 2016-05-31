import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from . import indent


class XmltvChannel(object):
    def __init__(self, channel_id):
        self._logger = logging.getLogger(__name__)
        self.root = Element(u"channel", {u"id": channel_id})

    def add_display_name(self, display_name):
        SubElement(self.root, u"display-name").text = display_name

    def save(self, fp, encoding=u"utf-8"):
        indent(self.root)
        ET.ElementTree(self.root).write(fp, encoding=encoding)
