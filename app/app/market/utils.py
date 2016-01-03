# encoding: utf-8

import re
import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup


class OpenGraph(dict):

    mandatory_attrs = ['title']
    required_attrs = ['title', 'type', 'image', 'url', 'description', 'site_name']
    article_attrs = ['author', 'published', 'published_time', 'published_date']

    def __init__(self, url, **kwargs):
        self.scrape = True
        self._url = url

        for k in kwargs.keys():
            self[k] = kwargs[k]

        dict.__init__(self)

        if url is not None:
            self.fetch(url)

    def __setattr__(self, name, val):
        self[name] = val

    def __getattr__(self, name):
        return self[name]

    def fetch(self, url):
        raw = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
        html = raw.read()
        return self.parser(html)

    def parser(self, html):
        if not isinstance(html, BeautifulSoup):
            doc = BeautifulSoup(html)
        else:
            doc = html
        ogs = doc.html.head.findAll(property=re.compile(r'^og'))
        for og in ogs:
            if og.has_attr(u'content'):
                self[og[u'property'][3:]] = og[u'content']

        # Couldn't fetch all attrs from og tags, try scraping body
        for attr in self.required_attrs:
            if not self.valid_attr(attr):
                try:
                    self[attr] = getattr(self, 'scrape_%s' % attr)(doc)
                except AttributeError:
                    pass

        # Get article attrs from og tags
        arts = doc.html.head.findAll(property=re.compile(r'^article'))
        arts_dict = {}
        for art in arts:
            if art.has_attr(u'content'):
                arts_dict[art[u'property'][8:]] = art[u'content']
        for attr in self.article_attrs:
            if not self.valid_attr(attr):
                try:
                    self[attr] = arts_dict[attr]
                except KeyError:
                    pass

    def valid_attr(self, attr):
        return hasattr(self, attr) and len(self[attr]) > 0

    def is_valid(self):
        return all([self.valid_attr(attr) for attr in self.mandatory_attrs])

    def scrape_image(self, doc):
        images = [dict(img.attrs)['src']
            for img in doc.html.body.findAll('img')]

        if images:
            return images[0]

        return u''

    def scrape_title(self, doc):
        return doc.html.head.title.text

    def scrape_type(self, doc):
        return 'other'

    def scrape_url(self, doc):
        return self._url

    def scrape_description(self, doc):
        tag = doc.html.head.findAll('meta', attrs={"name": "description"})
        result = "".join([t['content'] for t in tag])
        return result

    def scrape_site_name(self, doc):
        return urlparse(self._url).netloc


def fetch_graph_data(url):
    return OpenGraph(url=url)
