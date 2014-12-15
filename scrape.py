import requ.py

masterdict = {}
	pagecount = page_count()
	for i in range(1,pagecount):
		masterdict.update(index_scrape(i))

come_on = artist_scrape('http://nikitaxpvshkin.bandcamp.com')
print come_on
