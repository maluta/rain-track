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
    
	twitt = RaintrackTwitter().getPlaces()

	if twitt == None:
		pass
		# tratar erro

	geo_list = []
	comment_list = []
	self.map_point = []
	points = []
	
	# Added geoLocation info
	for place in places:	
		location = GeoLocation() 
		geo_list.append(location.getGeoLocation(place['address']))
		# save the comment list too
		comment_list.append(place['comment'])

	for i in len(places):
	
		points.append(geo_list[i]['latitude']) # lat
		points.append(geo_list[i]['longitude']) # lng
		points.append(comment_list[i]) # comment

		self.map_point.append(points)

	createMap()
		

		#self.response.out.write('Address: ' + place['address'] + '<br />')
		#self.response.out.write('Comment: ' + place['comment'] + '<br /><br />')

    # ------------------------------------------
    
def createMap(self):    
	self.response.headers['Content-Type'] = 'text/html'
	key = "ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg" # you will get your own key
    
	g = PyMap(key)                         # creates an icon & map by default
	icon2 = Icon('icon2')               # create an additional icon
	icon2.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
	icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
	g.addicon(icon2)
    
	g.maps[0].zoom = 15 # ...
    
	for i in len(self.map_points):
		g.maps[0].setpoint(self.map_points[i])               # add the points to the map
    
	self.response.out.write(g.showhtml())   
    
    # generate test file




def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
