__author__ = 'Adrian Strilchuk'

def indent(elem, level=0):
    """
    http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
    :param elem:
    :param level:
    :return:
    """
    i = u"\n" + level * u" "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + u" "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

from xmltvdocument import XmltvDocument
from xmltvchannel import XmltvChannel
from xmltvprogramme import XmltvProgramme
from xmltvwriter import XmltvWriter
