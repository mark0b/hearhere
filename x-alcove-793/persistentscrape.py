
import fs # find actual one


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
    while fs.exists('%s%d.%s' % (fname, i, ext)): # find actual fn
        i += 1
    return '%s%d.%s' % (fname, i, ext)


def lastfname(fname):
    pass


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

BANDS = 'bandurls.txt'
VISITED = 'visited.txt'
FAILED = 'failed.txt'
DATA = 'data.json'


bands = loadurlfile(BANDS)
visited = loadurlfile(VISITED)
failed = set()
queue = bands - visited
reid = re.compile(r'http://([^\.]+)\.bandcamp\.com')

# scrape urls
data = {}
while queue:
    url = queue.pop()
    try:
        id0 = reid.match(url).group(1)
        data[id0] = scrapeband(url)
        visited.add(url)
    except Exception():
        failed.add(url)

# write results of scrape
for (fname, text) in ((BANDS, bands), (VISITED, visited), (FAILED, failed), (DATA, data)):
    with open(freshfname(fname), 'w') as f:
        f.write(text)



