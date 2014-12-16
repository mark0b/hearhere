import urllib
import urllib2
import lxml.html as par

def page_count():
	#Find the number of pages in the artist index
	base_url = 'https://bandcamp.com/artist_index'
	page_num = 0
	init_res = urllib2.urlopen(base_url)
	tree = par.parse(init_res)
	root = tree.getroot()
	pages = root.find_class('pagenum')
	last = pages[-1]
	count_string = last.get('href')
	garbage, number = count_string.split('=')
	pagecount = int(number)
	return pagecount

def index_scrape(pagina):
	#Input and index page number
	#Output a dictionary with urls of bands on page as key
	#		and an empty dict as values
	base_url = 'https://bandcamp.com/artist_index?page='
	response = urllib2.urlopen(base_url+str(pagina))
	tree = par.parse(response)
	root = tree.getroot()
	result = root.get_element_by_id('bandlist')
	names = result.find_class('bandName')
	bands = {}
	band_elements = result.getiterator('a')
	for b in band_elements:
		bands[b.get('href')] = {}
	return bands

def artist_scrape(url):
	#Input bands bandcamp url
	#Output dictionary of information scraped from page
	#		info keys so far are: name, location,
	#		list of tags, most recent release date
	response = urllib2.urlopen(url)
	tree = par.parse(response)
	root = tree.getroot()

	#Is there a page here? Issue: xrobbiestone.bandcamp.com fixed
	try:
		result = root.get_element_by_id('band-name-location')
	except KeyError:
		return None

	info = {}
	info['loca'] = (result.find_class('location secondaryText')
		            [0].text)
	info['name'] = result.find_class('title')[0].text

	pagetype = root.get_element_by_id('rightColumn')
	#If band index page
	if ((pagetype.get('class') == 'rightColumn music-page ')
		or (pagetype.get('class') == 'rightColumn index-page')):
		#navigate to most recent album page
		album = (root.find_class('leftMiddleColumns')
					[0].find('.//a').get('href'))
		url0 = url + album
		response0 = urllib2.urlopen(url0)
		tree0 = par.parse(response0)
		root = tree0.getroot()

	ultra = root.get_element_by_id('discography')
	albums = ultra.find_class('trackTitle')
	releases = {}
	#If more releases than 1 gather info on all releases
	if len(albums) > 1:
		for a in albums:
			album_url = (a.find('.a').get('href'))
			url1 = url + album_url
			response1 = urllib2.urlopen(url1)
			tree1 = par.parse(response1)
			root1 = tree1.getroot()
			releases[album_url] = {}
			raw = []
			tags = root1.find_class('tag')
			for t in tags:
				raw.append(t.get('href'))
			releases[album_url]['tags'] = raw
			credits = root1.find_class('tralbumData tralbum-credits')
			date = credits[0].find('meta')
			if date == None:
				releases[album_url]['date'] = None
			else:
				releases[album_url]['date'] = (date.get('content'))
	else:
	    releases[albums[0].find('.//a').get('href')] = {}
	    raw = []
	    tags = root.find_class('tag')
	    for t in tags:
	    	raw.append(t.get('href'))
	    releases[albums[0].find('.//a').get('href')]['tags'] = (raw)
	    credits = root.find_class('tralbumData tralbum-credits')
	    releases[albums[0].find('.//a').get('href')]['date'] = (
	    			credits[0].find('meta').get('content'))
	
	info['releases'] = releases

	return info

if __name__ == '__main__':
	bands = index_scrape(0)
	for url in bands.keys():
		print url
		bands[url] = artist_scrape(url)
		print url, bands[url]
	print len(bands.keys())

	
	
	

