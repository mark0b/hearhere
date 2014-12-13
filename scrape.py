import requ.py

count = page_count()
	responses = []
	for i in range(0,count):
		responses.append(page_scrape(i))