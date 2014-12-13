import urllib
import urllib2
import lxml.html as par

def page_count():
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

def page_scrape(pagina):
	base_url = 'https://bandcamp.com/artist_index?page='
	response = urllib2.urlopen(base_url+str(pagina))
	tree = par.parse(response)
	root = tree.getroot()
	result = root.get_element_by_id('bandlist')
	names = result.find_class('bandName')
	bands = {}
	band_elements = result.getiterator('a')
	for b in band_elements:
		bands[b.get('href')] = b.find_class('bandName')[0].text
	return bands


if __name__ == '__main__':
	masterdict = {}
	pagecount = page_count()
	for i in range(1,pagecount):
		masterdict.update(page_scrape(0))
	print masterdict
	

