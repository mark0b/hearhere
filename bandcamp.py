from urllib2 import urlopen
from lxml.html import parse

# TODO handle HTTP errors in urlopen
# TODO add back fields to scrapeband
# TODO add logging support


def scrapeindexes():
    """crawl the bandcamp artist listings for all the band urls"""

    print 'scrapeindexes'

    # get the number of pages
    html = urlopen('https://bandcamp.com/artist_index')
    e = parse(html).getroot().find_class('pagenum').pop()
    numpages = int(e.text_content())

    # scrape each index page for band urls
    bands = set()
    for i in range(1, maxi or numpages + 1):
        html = urlopen('https://bandcamp.com/artist_index?page=%d' % i)
        print i
        bandlist = parse(html).getroot().get_element_by_id('bandlist')
        bands |= {a.get('href') for a in bandlist.getiterator('a')}



def scrapeband(url):
    """scrapes a bandcamp band page for the band's info"""

    print 'scrapeband'

    root = parse(urlopen(url)).getroot()
    eloc = root.get_element_by_id('band-name-location')
    return {
        'location': e.find_class('location secondaryText')[0].text,
        'name': e.find_class('title')[0].text,
        'tags': [a.get('href') for a in root.find_class('tag')]
    }



def scrape():
    urls = scrapeindexes()
    data = {url: scrapeband(url) for url in urls}
    return data



if __name__ == '__main__':
    print scrape()


