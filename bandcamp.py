#!/usr/bin/env python

import urllib2
import re
from lxml.html import parse
from json import dumps as tojson
from time import sleep






def urlopen(url, attempts=3):
    """returns the html from a url or None if all attempts fail"""

    if attempts == 0:
        # TODO add app engine logging
        return None
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError:
        sleep(10) # secs
        return urlopen(url, attempts - 1)





def scrapeindexes():
    """crawl the bandcamp artist listings for all the band urls"""

    # get the number of pages
    html = urlopen('https://bandcamp.com/artist_index')
    if html is None: return None
    e = parse(html).getroot().find_class('pagenum').pop()
    numpages = int(e.text_content())

    # scrape each index page for band urls
    bands = set()
    for i in range(1, 2 or numpages + 1):
        html = urlopen('https://bandcamp.com/artist_index?page=%d' % i)
        bandlist = parse(html).getroot().get_element_by_id('bandlist')
        bands |= {a.get('href') for a in bandlist.getiterator('a')}

    return bands



def scrapeband(url):
    """scrapes a bandcamp band page for the band's info"""

    html = urlopen(url)
    if html is None: return None
    root = parse(html).getroot()
    e = root.get_element_by_id('band-name-location', None)
    if e is None: return None

    return {
        # TODO add back fields
        'location': e.find_class('location secondaryText')[0].text,
        'name': e.find_class('title')[0].text,
        'tags': [a.get('href') for a in root.find_class('tag')]
    }



def scrape():
    urls = scrapeindexes()
    data = {url: scrapeband(url) for url in urls}
    return {url: data[url] for url in data if data[url]}



if __name__ == '__main__':
    print tojson(scrape())


