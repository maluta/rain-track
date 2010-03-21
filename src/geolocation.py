# -*- coding: utf-8 -*-
#!/bin/python

import sys
from geopy import geocoders  

APIKEY="ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg"

class GeoLocation:
	def __init__(self):
		g = geocoders.Google(APIKEY);

	def getGeoLocation(self, address):
		g = geocoders.Google(APIKEY);
		# fazer try - catch
#		print "(",address,")"
		place, (lat, lng) = g.geocode(address)
		return { 'latitude':lat , 'longitude':lng  } 
		


