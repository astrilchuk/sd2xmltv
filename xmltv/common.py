#!/usr/bin/python
# coding=utf-8

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime, time
import logging

class XmltvDocument(object):

    def __init__(self):
        self.root = Element('tv')
        self._logger = logging.getLogger(__name__)

    def add_channel(self, channel_id):
        self._logger.debug('add_channel("%s")' % (channel_id))
        return XmltvChannel(self.root, channel_id)

    def add_programme(self, start_time, stop_time, channel):
        self._logger.debug('add_programme(%s, %s, %s)' % (start_time, stop_time, channel))
        return XmltvProgramme(self.root, start_time, stop_time, channel)

    def has_channel(self, channel_id):
        return self.root.find('./channel[@channel="%s"]' % (channel_id)) is not None

    def save(self, path):
        indent(self.root)
        ET.ElementTree(self.root).write(path, xml_declaration=True)
        #self.root.save(path)

class XmltvChannel(object):

    def __init__(self, root, channel_id):
        self.root = SubElement(root, 'channel', { 'id' : channel_id })

    def add_display_name(self, display_name):
        SubElement(self.root, 'display-name').text = display_name

class XmltvProgramme(object):

    def __init__(self, root, start_time, stop_time, channel_id):
        attribs = {
            'start' : start_time.strftime('%Y%m%d%H%M%S %z').strip(),
            'stop' : stop_time.strftime('%Y%m%d%H%M%S %z').strip(),
            'channel' : channel_id }
        self.root = SubElement(root, 'programme', attribs)
        self._credits = None

    def add_title(self, title, lang = None):
        attr = { }
        if lang is not None:
            attr = { 'lang' : lang }
        SubElement(self.root, 'title', attr).text = title

    def add_subtitle(self, subtitle, lang = None):
        attr = { }
        if lang is not None:
            attr = { 'lang' : lang }
        SubElement(self.root, 'sub-title', attr).text = subtitle

    def add_category(self, category, lang = None):
        attr = { }
        if lang is not None:
            attr = { 'lang' : lang }
        SubElement(self.root, 'category', attr).text = category

    def add_description(self, description, lang = None):
        attr = { }
        if lang is not None:
            attr = { 'lang' : lang }
        SubElement(self.root, 'desc', attr).text = description

    def add_date(self, date):
        SubElement(self.root, 'date').text = date

    def add_category(self, category, lang = None):
        attr = { }
        if lang is not None:
            attr = { 'lang' : lang }
        SubElement(self.root, 'category', attr).text = category

    def add_episode_num(self, system, episode_num):
        SubElement(self.root, 'episode-num', { 'system' : system }).text = episode_num

    def add_episode_num_onscreen(self, episode):
        self.add_episode_num('onscreen', episode)

    def add_episode_num_xmltv_ns(self, season_num = None, total_seasons = None, episode_num = None, total_episodes = None, part_num = None, total_parts = None):
        e = ''
        if season_num is not None:
            e += str(season_num - 1)
            if total_seasons is not None:
                e = '{0}/{1}'.format(e, str(total_seasons))
        e += '.'
        if episode_num is not None:
            e += str(episode_num - 1)
            if total_episodes is not None:
                e = '{0}/{1}'.format(e, str(total_episodes))
        e += '.'
        if part_num is not None:
            e += str(part_num - 1)
            if total_parts is not None:
                e = '{0}/{1}'.format(e, str(total_parts))
        self.add_episode_num('xmltv_ns', e)

    def add_episode_num_dd_progid(self, tms_id):
        self.add_episode_num('dd_progid', tms_id[:-4] + '.' + tms_id[-4:])

    def add_credit(self, credit_type, credit):
        if self._credits is None:
            self._credits = SubElement(self.root, 'credits')
        if credit_type in ['actor', 'presenter']:
            SubElement(self._credits, credit_type).text = credit

    def add_credit_director(self, credit):
        self.add_credit('director', credit)

    def add_credit_actor(self, credit):
        self.add_credit('actor', credit)

    def add_credit_writer(self, credit):
        self.add_credit('writer', credit)

    def add_credit_adapter(self, credit):
        self.add_credit('adapter', credit)

    def add_credit_producer(self, credit):
        self.add_credit('producer', credit)

    def add_credit_composer(self, credit):
        self.add_credit('composer', credit)

    def add_credit_editor(self, credit):
        self.add_credit('editor', credit)

    def add_credit_presenter(self, credit):
        self.add_credit('presenter', credit)

    def add_credit_commentator(self, credit):
        self.add_credit('commentator', credit)

    def add_credit_guest(self, credit):
        self.add_credit('guest', credit)

    def add_rating(self, rating_system, rating):
        ratingElement = SubElement(self.root, 'rating', {'system': rating_system})
        SubElement(ratingElement, 'value').text = rating

    def add_star_rating(self, rating, max_rating, system=None):
        attr = { }
        if system is not None:
            attr = {'system': system }
        element = SubElement(self.root, 'star-rating', attr)
        SubElement(element, 'value').text = '%s/%s' % (rating, max_rating)

    def add_new(self):
        SubElement(self.root, 'new')

def indent(elem, level=0):
    """
    http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
    :param elem:
    :param level:
    :return:
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
