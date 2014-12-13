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
	last = pages[len(pages)-1]
	count_string = last.get('href')
	garbage, number = count_string.split('=')
	pagecount = int(number)
	return pagecount

def page_scrape(pagina):
	base_url = 'https://bandcamp.com/artist_index?page='
	response = urllib2.urlopen(base_url+str(pagina))
	tree = par.parse(response)
	root = tree.getroot()
	elements = root.find_class('bandName')
	bands = {}
	for i in range(0,len(elements)-1):
		print elements[i].keys()
		print elements[i].items()
		print elements[i].get('class')
		bands[elements[i].get('bandName')] = elements[i].get('href')
	return bands


if __name__ == '__main__':
	bands = page_scrape(0)
	print bands
	

