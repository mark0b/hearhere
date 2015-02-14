#!/usr/bin/env python

import urllib2
import re
import logging
from lxml.html import parse
from json import dumps as tojson
from time import sleep



def getlatlng(place):
    """gets the lat lng from the google maps places api"""

    # TODO implement this
    return place



def urlopen(url, attempts=3):
    """returns the html from a url or None if all attempts fail"""

    if attempts == 0:
        logging.warning("could not access %s" % url)
        # TODO add app engine logging
        return None
    try:
        return urllib2.urlopen(url)
    except urllib2.URLError:
        sleep(10) # secs
        return urlopen(url, attempts - 1)





def scrapeindexes():
    """generate band urls by scraping bandcamp artist indexes"""

    # get the number of pages
    html = urlopen('https://bandcamp.com/artist_index')
    if html is None: return
    e = parse(html).getroot().find_class('pagenum').pop()
    numpages = int(e.text_content())
    reurl = re.compile(r'http://([^\.]+)\.bandcamp\.com')

    # scrape each index page for band urls
    for i in range(1, numpages + 1):
        html = urlopen('https://bandcamp.com/artist_index?page=%d' % i)
        bandlist = parse(html).getroot().get_element_by_id('bandlist')
        for a in bandlist.getiterator('a'):
            url = a.get('href')
            if reurl.match(url):
                yield url
                sleep(1)




def scrapeband(url):
    """scrapes a bandcamp band page for the band's info"""

    html = urlopen(url)
    if html is None: return
    root = parse(html).getroot()
    e = root.get_element_by_id('band-name-location', None)
    if e is None: return

    return {
        # TODO add back fields
        # TODO possible problem with unicode values
        'location': e.find_class('location secondaryText')[0].text,
        'name': e.find_class('title')[0].text,
        'tags': [a.text_content() for a in root.find_class('tag')]
    }




def scrape():
    # TODO only scrape newest artists who haven't be scraped before
    reid = re.compile(r'http://([^\.]+)\.bandcamp\.com')
    data = {reid.match(url).group(1): scrapeband(url) for url in scrapeindexes()}
    return {id0: data[id0] for id0 in data if data[id0]}




if __name__ == '__main__':
    print tojson(scrape())


