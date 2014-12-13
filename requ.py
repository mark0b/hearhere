import urllib
import urllib2
import lxml.html

def request():
	base_url = 'https://bandcamp.com/artist_index'
	page_num = 0
	responses = []
	init_res = urllib2.urlopen(base_url)
	html = init_res.read()

	return

if __name__ == '__main__':
	stuff = request()
	

