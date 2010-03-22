# -*- coding: utf-8 -*-
#!/bin/python

import sys
from geopy import geocoders  

#APIKEY="ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBQAVO7ySHh3DH1ywcKBZ_iu3D-xWhRMPHBlEkwjYlzbs7Y73KlRJrMHcA"
APIKEY="ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg"

class GeoLocation:
	def __init__(self):
		self.g = geocoders.Google(APIKEY);

	def getGeoLocation(self, address):
		self.g = geocoders.Google(APIKEY);
		# fazer try - catch
#		print "(",address,")"
		place, (lat, lng) = self.g.geocode(address)
		return { 'latitude':lat , 'longitude':lng  } 
		


