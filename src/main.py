#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from pymaps import *
from raintracktwitter import *
from geopy import geocoders  
from geolocation import * 

class MainHandler(webapp.RequestHandler):

	def get(self):
    
		lugares = RaintrackTwitter().getPlaces()

		#print lugares

		if lugares == None:
		#	print ".."
			pass
			# tratar erro

		geo_list = {}
		comment_list = []
		self.map_points = []
		points = []
	
		# Added geoLocation info
		for place in lugares:
		#	print "place",place
			location = GeoLocation()
			s = place['address']
		#	print s
			geo_list = location.getGeoLocation(s)
			# save the comment list too
			comment_list.append(place['comment'])
			

		count=0

		for i in lugares:
	
			points.append(geo_list['latitude']) # lat
			points.append(geo_list['longitude']) # lng
#			points.append(comment_list[i]) # comment

			count +=1


		for i in range(count):

			l = geo_list['latitude']
			ll = geo_list['longitude']
		
			self.map_points.append(l)
			self.map_points.append(ll)

		self.createMap()

		#self.response.out.write('Address: ' + place['address'] + '<br />')
		#self.response.out.write('Comment: ' + place['comment'] + '<br /><br />')

    # ------------------------------------------
    
	def createMap(self):    
		self.response.headers['Content-Type'] = 'text/html'
		key = "ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg" # you will get your own key
    
		g = PyMap(key)                         # creates an icon & map by default
		
		g.setLat(self.map_points[0])
		g.setLong(self.map_points[1])

		icon2 = Icon('icon2')               # create an additional icon
		icon2.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
		icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
		g.addicon(icon2)
    
		g.maps[0].zoom = 15 # ...
    
    		l = []
		v = len(self.map_points)/2;

		for i in range(v):

			l.append(self.map_points[i])
			l.append(self.map_points[i+1])

			g.maps[0].setpoint(l)               # add the points to the map

			l = []
    
		self.response.out.write(g.showhtml())   
    
    # generate test file




def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
