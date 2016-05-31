import logging
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from . import indent


class XmltvProgramme(object):
    def __init__(self, start_time, stop_time, channel_id):
        self._logger = logging.getLogger(__name__)
        attr = {
            u"start": unicode(start_time.strftime("%Y%m%d%H%M%S")),
            u"stop": unicode(stop_time.strftime("%Y%m%d%H%M%S")),
            u"channel": channel_id}
        self.root = Element(u"programme", attr)
        self._credits = None

    def add_title(self, title, lang=None):
        attr = {}
        if lang is not None:
            attr = {u"lang": lang}
        SubElement(self.root, u"title", attr).text = title

    def add_subtitle(self, subtitle, lang=None):
        attr = {}
        if lang is not None:
            attr = {u"lang": lang}
        SubElement(self.root, u"sub-title", attr).text = subtitle

    def add_category(self, category, lang=None):
        attr = {}
        if lang is not None:
            attr = {u"lang": lang}
        SubElement(self.root, u"category", attr).text = category

    def add_description(self, description, lang=None):
        attr = {}
        if lang is not None:
            attr = {u"lang": lang}
        SubElement(self.root, u"desc", attr).text = description

    def add_date(self, date):
        SubElement(self.root, u"date").text = date

    def add_episode_num(self, system, episode_num):
        SubElement(self.root, u"episode-num", {u"system": system}).text = episode_num

    def add_episode_num_onscreen(self, episode):
        self.add_episode_num(u"onscreen", episode)

    def add_episode_num_xmltv_ns(self, season_num=None, total_seasons=None, episode_num=None, total_episodes=None, part_num=None, total_parts=None):
        e = u""
        if season_num is not None:
            e += unicode(season_num - 1)
            if total_seasons is not None:
                e = u"{0}/{1}".format(e, total_seasons)
        e += u"."
        if episode_num is not None:
            e += unicode(episode_num - 1)
            if total_episodes is not None:
                e = u"{0}/{1}".format(e, total_episodes)
        e += u"."
        if part_num is not None:
            e += unicode(part_num - 1)
            if total_parts is not None:
                e = u"{0}/{1}".format(e, total_parts)
        self.add_episode_num(u"xmltv_ns", e)

    def add_episode_num_dd_progid(self, tms_id):
        self.add_episode_num(u"dd_progid", u"{0}.{1}".format(tms_id[:-4], tms_id[-4:]))

    def add_previously_shown(self, start=None, channel=None):
        attr = {}
        if start is not None:
            attr.update({u"start": unicode(start.strftime("%Y%m%d"))})
        if channel is not None:
            attr.update({u"channel": channel})
        SubElement(self.root, u"previously-shown", attr)

    def add_credit(self, credit_type, credit):
        if self._credits is None:
            self._credits = SubElement(self.root, u"credits")
        if credit_type in [u"actor", u"presenter"]:
            SubElement(self._credits, credit_type).text = credit

    def add_credit_director(self, credit):
        self.add_credit(u"director", credit)

    def add_credit_actor(self, credit):
        self.add_credit(u"actor", credit)

    def add_credit_writer(self, credit):
        self.add_credit(u"writer", credit)

    def add_credit_adapter(self, credit):
        self.add_credit(u"adapter", credit)

    def add_credit_producer(self, credit):
        self.add_credit(u"producer", credit)

    def add_credit_composer(self, credit):
        self.add_credit(u"composer", credit)

    def add_credit_editor(self, credit):
        self.add_credit(u"editor", credit)

    def add_credit_presenter(self, credit):
        self.add_credit(u"presenter", credit)

    def add_credit_commentator(self, credit):
        self.add_credit(u"commentator", credit)

    def add_credit_guest(self, credit):
        self.add_credit(u"guest", credit)

    def add_rating(self, rating_system, rating):
        element = SubElement(self.root, u"rating", {u"system": rating_system})
        SubElement(element, u"value").text = rating

    def add_star_rating(self, rating, max_rating, system=None):
        attr = {}
        if system is not None:
            attr = {u"system": system}
        element = SubElement(self.root, u"star-rating", attr)
        SubElement(element, u"value").text = u"{0}/{1}".format(rating, max_rating)

    def add_new(self):
        SubElement(self.root, u"new")

    def add_icon(self, src):
        SubElement(self.root, u"icon", {u"src": src})

    def save(self, fp, encoding=u"utf-8"):
        indent(self.root)
        ET.ElementTree(self.root).write(fp, encoding=encoding)
