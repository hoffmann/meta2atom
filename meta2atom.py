#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
meta2atom is a python script to generate atom feeds from the meta data
in html pages"""

import sys
import lxml.html
import feedparser
import datetime
import lxml.etree as ET

# http://henry.precheur.org/2008/9/3/RFC 3339 formatting in Python.html
from rfc3339 import rfc3339

import logging



class Page(object):
    def __init__(self, filename_or_url, url):
        """extract html meta data from a filename, url or file like
        object.
        
        filename_or_url: source where to read content from
        url: url for this page, this should be the url for the element
        """
        self.tree = lxml.html.parse(filename_or_url)
        self.meta = self.tree.findall("/head/meta")
        self.url = url

    def _get_meta(self, name):
        name = name.lower()
        for elem in self.meta:
            metaname = elem.get("name", "").lower()
            if metaname == name:
                content =  elem.get("content")
                if content != "":
                    return content
        return None

    def _get_meta_title(self):
        title = self.tree.find("/head/title")
        if title is not None:
            return title.text_content()
        return None 

    def _get(self, *names):
        """for name in names try to get meta information. 
        Returns None if no meta information is found"""
        for name in names:
            meta = self._get_meta(name)
            if meta:
               return meta
        return None

    @property
    def title(self):
        title = self._get_meta_title()
        if title is None:
            title = self._get_meta("DC.title")
        return title

    @property
    def author(self):
        return self._get("DC.creator", "author")

    @property
    def description(self):
        return self._get("DC.description", "description")

    @property
    def keywords(self):
        #TODO handle DC.Subject.Keywords
        keywords = self._get("DC.subject", "keywords")
        if keywords:
            return [x.strip() for x in keywords.split(",")]
        return None

    @property
    def date(self):
        #TODO use http://labix.org/python-dateutil instead of feedparser
        d = self._get("DC.date", "date")
        if d:
            #TODO ??? timezone
            timetuple = feedparser._parse_date(d)
            return datetime.datetime(*timetuple[:7])
        return None 


def page2element(page, baseurl):
    root = ET.Element("entry")

    if page.author:
        author = ET.SubElement(root, "author")
        name = ET.SubElement(author,"name")
        name.text = page.author
    title = ET.SubElement(root, "title")
    title.text = page.title
    ET.SubElement(root, "link", attrib={"rel":"alternate", "type":"text/html",  "href":page.url})
    
    id = ET.SubElement(root, "id")
    #TODO generate id
    id.text = page.url

    summary = ET.SubElement(root, "summary")
    if page.description:
        summary.text = page.description
    else:
        logging.warn("Missing summary for element %s using title instead" %page.url)
        summary.text = page.title
    
    date = ET.SubElement(root, "updated")
    if page.date:
        #TODO check if right format 
        date.text = rfc3339(page.date)
    else:
        logging.warn("Missing date for element %s using now() instead" %page.url)
        date.text = rfc3339(datetime.datetime.now())
   
    if page.keywords:
        for keyword in page.keywords:
            ET.SubElement(root, "category", attrib={"scheme":baseurl, "term":keyword})

    return root


class AtomGenerator(object):
    def __init__(self, baseurl, feedurl, title,  name, pages, email=None, summary=None):
        self.baseurl = baseurl
        self.feedurl = feedurl
        self.title = title
        self.name = name
        self.pages = pages
        self.email = email
        self.summary = summary


    def gen_atom(self):
        #pages, title, baseurl, feedurl, name, email=None, summary=None):
        feed = ET.Element("feed", nsmap={None: 'http://www.w3.org/2005/Atom'})
        #TODO set namespace

        f_title = ET.SubElement(feed, "title")
        f_title.text = self.title

        f_id = ET.SubElement(feed, "id")
        #TODO generate id
        f_id.text = self.feedurl
       
        f_updated = ET.SubElement(feed, "updated")
        f_updated.text = rfc3339(datetime.datetime.now())

        ET.SubElement(feed, "link", attrib={"href":self.feedurl, "rel":"self"})
        ET.SubElement(feed, "link", attrib={"href":self.baseurl})

        f_author = ET.SubElement(feed, "author")
        f_name = ET.SubElement(f_author, "name")
        f_name.text = self.name
        if self.email:
            f_email = ET.SubElement(f_author, "email")
            f_email.text = self.email

        if self.summary:
            f_summary = ET.SubElement(feed, "summary")
            f_summary.text = self.summary
        
        for page in self.pages:
            elem = page2element(page, self.baseurl)
            feed.append(elem)

        return feed

    def to_string(self):
        return lxml.etree.tostring(self.gen_atom(), pretty_print=True)

def test():
    baseurl = "http://peter-hoffmann.com"
    feedurl = "http://peter-hoffmann.com/test/atom.xml"
    title = "Peter Hoffmanns Feed"
    name = "Peter Hoffmann"
    email = "tosh54@gmail.com"

    import glob
    pages = []
    for p in glob.glob("test/*.html"):
        page = Page(p, "http://peter-hoffmann.com/"+p)
        pages.append(page)

    generator = AtomGenerator(baseurl, feedurl, title, name, pages, email)

    #feed = generator.gen_atom()

    print generator.to_string()

def main(argv=None):
    if argv is None:
        argv = sys.argv

    test()

if __name__ == "__main__":
    main()

