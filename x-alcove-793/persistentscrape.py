from urllib2 import urlopen
from os.path import isfile
from json import dumps as tojson
from time import sleep
import re


def loadurlfile(fname):
    reurl = re.compile(r'http://([^\.]+)\.bandcamp\.com')
    with open(fname, 'r') as f:
        return set(filter(reurl.match, f.read().split('\n')))


def saveurlfile(fname, urls):
    with open(fname, 'w') as f:
        f.write('\n'.join(urls))


def freshfname(fname):
    parts = fname.split('.')
    (ext, fname) = (parts.pop(), '.'.join(parts))
    i = 0
    while isfile('%s%d.%s' % (fname, i, ext)): # find actual fn
        i += 1
    return '%s%d.%s' % (fname, i, ext)



def scrapeband(url):
    """scrapes a bandcamp band page for the band's info"""

    html = urlopen(url)
    sleep(1)
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

reurl = re.compile(r'http://([^\.]+)\.bandcamp\.com')

def htmlread(url):
    match = reurl.match(url)
    if not match:
        return
    id0 = match.group(1)
    if isfile(id0 + '.html'):
        return
    html = urlopen(url)
    sleep(1)
    if not html:
        raise Exception()
    with open('html/%s.html' % (id0,) ,'w') as f:
        f.write(html.read())
    

if __name__ == '__main__':
    with open('bandurls.txt', 'r') as urls:
        with open('log.txt', 'w') as log:
            for url in urls:
                try:
                    htmlread(url)
                except Exception():
                    log.write(url + '\n')


def bands():    
    BANDS = 'bandurls.txt'
    VISITED = 'visited.txt'
    FAILED = 'failed.txt'
    DATA = 'data.json'


    bands = loadurlfile(BANDS)
    visited = loadurlfile(VISITED)
    failed = set()
    queue = bands - visited
    

    # scrape urls
    data = {}
    while queue:
        url = queue.pop()
        try:
            id0 = reurl.match(url).group(1)

            #data[id0] = scrapeband(url)
            visited.add(url)
        except Exception():
            failed.add(url)

    # write results of scrape
    # for (fname, urls) in ( (VISITED, visited), (FAILED, failed)):
    #     saveurlfile(fname,urls)

    # with open(freshfname('data.json'), 'w') as f:
    #     f.write(tojson(data))






