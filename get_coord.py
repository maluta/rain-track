# -*- coding: utf-8 -*-


#!/bin/python
import sys
from geopy import geocoders  

APIKEY="ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg"


address = sys.argv[1]

print "buscando por: ",address

g = geocoders.Google(APIKEY);
#place, (lat, lng) = g.geocode("Av. Engenheiro Eusebio Stevaus, 823 ") 
place, (lat, lng) = g.geocode(address) 
print "%s: %.5f, %.5f" % (place, lat, lng) 


