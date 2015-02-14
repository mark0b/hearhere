
from google.appengine.ext import ndb




# use http://stackoverflow.com/questions/18508780/finding-all-the-locations-in-a-given-radius-using-google-app-engine-gql
class Location(ndb.Model):
	"""Models a location with a lat, lng"""
	loc = ndb.GeoPtProperty

	@staticmethod
	def inrange(minlat, minlng, maxlat, maxlng):





class QuadTreeNode:

	def __init__(self, bounds):
		self.bounds = bounds
		self.northwest = None
		self.northeast = None
		self.southwest = None
		self.southeast = None


	def add(self, loc):
		inrange = lamdba n, (low, high): n > low and n < high
		(lat, lng) = loc
		((minlat, minlng), (maxlat, maxlng)) = self.bounds
		if inrange(lat, )


		if type() == 


		if leaf.lat > self.centerlat:
			if leaf.lng > self.centerlng:
				i = 0 # upper right
			else:
				i = 1 # upper left
		else:
			if leaf.lng > self.centerlng:
				i = 2 # lower right
			else:
				i = 3 # lower left
		if type(self.children[i]) == type(None):
			self.minlat =


		if type(self.children[k]) == type(None):
			if k in {'upperleft', 'upperright'}:


			maxlat = self.maxlat if k in {'upperleft', 'upperright'} else self.centerlat
			minlat = self.minlat if k in {'lowerleft', 'lowerright'} else 

		if type(self.children[k]) == QuadTreeNode:
			self.children[k].add(leaf)



class QuadTreeLeaf:

	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng







