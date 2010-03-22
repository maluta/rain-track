#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

class YahooMapsHandler(webapp.RequestHandler):
  
  def getGeolocation(self, address):
    
    # Query latitude and longitude for this address
    APIKEY="ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg" # ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBQAVO7ySHh3DH1ywcKBZ_iu3D-xWhRMPHBlEkwjYlzbs7Y73KlRJrMHcA

    place, (lat, lng) = geocoders.Google().geocode(address)
    
    geolocation = { 
      'latitude': lat, 
      'longitude': lng 
    }
    
    return geolocation
    
  
  def get(self):
    
    query = self.request.get('query');

    

    if query:
      query = "#raintrack " + query
    else:
      query = "#raintrack"
    
    
    places = RaintrackTwitter(query).getPlaces()
    
    if not places:
      self.response.out.write('No #raintrack messages found.')
      return

    html = u'''
      <html>
	<head>
	<script type="text/javascript" src="http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=quNejkLV34GTmULC_bW9QlSlNPLyTnTstYyQTm9CocrBzBv45y40lRy7NZJYr7t2mEYyb_l3LADT"></script>
	<style type="text/css">
	#map{
		height: 75%;
		width: 100%;
	}
	</style>
	</head>
	<body>
	<div id="map"></div>
	<script type="text/javascript">
		// Create a Map that will be placed in the "map" div.
		var map = new YMap(document.getElementById('map')); 
		
		// Create an array to contain the points of our polyline
		polylinePoints = [];
		
		function startMap(){
			
			map.addTypeControl(); 	
			map.addZoomLong();    		
			map.addPanControl();  
			map.drawZoomAndCenter("Sao Paulo, SP", 7);
			
			function placeRainMarker(lat, lng, comment) {

				geoPoint = new YGeoPoint(lat, lng, comment);

				var newMarker= new YMarker(geoPoint, createCustomMarkerImage());
				newMarker.addAutoExpand(comment);
				var markerMarkup = "<b>" + comment + "</b>";
				
				YEvent.Capture(newMarker, EventsList.MouseClick, 
					function(){
						newMarker.openSmartWindow(markerMarkup);
					});
				map.addOverlay(newMarker);
			}

			function createCustomMarkerImage(){
				var myImage = new YImage();
				myImage.src = '/images/cloud_icon.png';
				myImage.size = new YSize(20,20);
				myImage.offsetSmartWindow = new YCoordPoint(0,0);
				return myImage;	
			}
	  
	'''.encode("utf8", 'ignore')
	
    
    for place in places:
      #self.response.out.write('Address: ' + place['address'] + '<br />')
      #self.response.out.write('Comment: ' + place['comment'] + '<br />')
      
      place_geoloc = self.getGeolocation( place['address'].encode("utf8", 'ignore')  )
      #self.response.out.write('Latitude: ' + str(place_geoloc['latitude']) + '<br />')
      #self.response.out.write('Longitude: ' + str(place_geoloc['longitude']) + '<br /><br />')

      html += 'placeRainMarker(' + str(place_geoloc['latitude']) + ', ' + str(place_geoloc['longitude']) + ", '" + place['comment'].encode("utf8", 'ignore') + "');\n"
      
    html += '''
    
	      }	

	window.onload = startMap;

	</script>
	</body>
	</html>
    '''.encode("utf8", 'ignore')
  
	  
    self.response.out.write(html)
	  
	  
	  
	  
	  
	  
	  

class GoogleMapsHandler(webapp.RequestHandler):

	def getGeolocation(self, address):
	
	    # Query latitude and longitude for this address
	    #APIKEY="ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg" # 
	    
	    APIKEY="ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBRlOb26qSyU154aZeLwOrF4C7-DphRAQ6j2zPzZSsgdymxmiQGql6gz3w"
	    #APIKEY="ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBQAVO7ySHh3DH1ywcKBZ_iu3D-xWhRMPHBlEkwjYlzbs7Y73KlRJrMHcA"
	    #APIKEY="ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg"
	    place, (lat, lng) = geocoders.Google(APIKEY).geocode(address)
	    
	    geolocation = { 
	      'latitude': lat, 
	      'longitude': lng 
	    }
	
	    return geolocation

	def get(self):
    
		query = self.request.get('query');
		
		if query:
		  query = "#raintrack " + query
		else:
		  query = "#raintrack"
		
    
		lugares = RaintrackTwitter(query).getPlaces()

		if not lugares:
		  self.response.out.write('No #raintrack messages found.')
		  return

		geo_list = {}
		self.comment_list = []
		self.map_points = []
		points = []
		count=0

		# Added geoLocation info
		for place in lugares:
		#	print "place",place
			#location = GeoLocation()
			s = place['address'].encode("utf8", 'ignore')
			#geo_list = location.getGeolocation(s)
			geo_list = self.getGeolocation(s)
			# save the comment list too
			self.comment_list.append(place['comment'])
	
			points.append(geo_list['latitude']) # lat
			points.append(geo_list['longitude']) # lng


			count +=1
			
		self.map_points = points
		
		self.createMap()

    # ------------------------------------------
    
	def createMap(self):    
		self.response.headers['Content-Type'] = 'text/html'
		#key = "ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBQAVO7ySHh3DH1ywcKBZ_iu3D-xWhRMPHBlEkwjYlzbs7Y73KlRJrMHcA"
		#key = "ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBQAVO7ySHh3DH1ywcKBZ_iu3D-xWhRMPHBlEkwjYlzbs7Y73KlRJrMHcA"
		key = "ABQIAAAAACsLwZOSYc-_FsQ-H_0uGBRlOb26qSyU154aZeLwOrF4C7-DphRAQ6j2zPzZSsgdymxmiQGql6gz3w"
		g = PyMap(key)                         # creates an icon & map by default
		
		g.setLat(self.map_points[0])
		g.setLong(self.map_points[1])

		icon2 = Icon('icon2')               # create an additional icon
		icon2.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
		icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
		g.addicon(icon2)
    
		g.maps[0].zoom = 8	# ...
 
#		print self.map_points

		c=0
		for i in range(0,len(self.map_points),2):
		# a função setpoint recebe [lat,long,..,..] (no minimo os 2 primeiros)
			x = self.map_points[i:i+2]
			x.append(self.comment_list[c])
			c+=1
			g.maps[0].setpoint(x) 

#		q = [-21.58992, -26.66208, '#raintrack'] # test only
#		g.maps[0].setpoint(q) 

		self.response.out.write(g.showhtml())   
    
    # generate test file


class IndexHandler(webapp.RequestHandler):
  
  def get(self):
	html = '''
	<html>
	      <head>
		    <title>rain-track</title>
		    
		    <script type="text/javascript">
			  function submit()
			  {
				var engine1 = document.getElementById("service1");
				var engine2 = document.getElementById("service2");
				var q = document.getElementById("query").value;

				if (engine1.checked)
				{
				      document.getElementById("map").src = "http://rain-track.appspot.com/yahoo?query=" + q;
				}
				else if (engine2.checked)
				{
				      document.getElementById("map").src = "http://rain-track.appspot.com/google?query=" + q;
				}
			  }
		    </script>
	      </head>
	      
	      <body>
		    <center>
		    <div style="width:1024px; height:768px">
			  <div style="width:340px; height:135px; position:relative; left:-300px">
				<img src="/images/logotipo_transparent.png" alt="rain-track" width="340px" height="135px" />
			  </div>
			  <div style="width:70%; height:150px; position:relative; left:220px; top:-150px; text-align:center">
				<br /><br />
				<b>Local: </b><input type="text" id="query" name="location" size="50" />
				<input type="submit" value="GO!" onclick="submit()" />
				<br /><br />
				<form>
				      <label for="yahoo">Yahoo! Maps</label>
				      <input type="radio" name="service" value="yahoo" id="service1" checked="true" />
				      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				      <label for="google">Google Maps</label>
				      <input type="radio" name="service" value="google" id="service2" />
				</form>
			  </div>
			  
			  <center>
			  <div style="width:100%; height:70%; text-align:center; vertical-align:middle; position:relative; top:-17%">
				<center>
				<div style="width:95%; height:100%">
				      <iframe id="map" style="width:100%; height:100%" frameborder="0" scrolling="no">
					    
				      </iframe>
				</div>
				</center>
			  </div>
			  </center>
		    </div>
		    </center>
	      </body>
	</html>
	'''.encode("utf8", 'ignore')
	
	self.response.out.write(html)


def main():
  application = webapp.WSGIApplication([('/', IndexHandler),
					('/google', GoogleMapsHandler),
					('/yahoo',  YahooMapsHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
