#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from raintracktwitter import RaintrackTwitter
      
# --------------------------------------------------------------------------- #
# Request Handler
# --------------------------------------------------------------------------- #

class MainPage(webapp.RequestHandler):
  
  def get(self):
    
    places = RaintrackTwitter().getPlaces()
    
    if not places:
      self.response.out.write('No #raintrack messages found.')
      return
    
    for place in places:
      self.response.out.write('Address: ' + place['address'] + '<br />')
      self.response.out.write('Comment: ' + place['comment'] + '<br /><br />')


# --------------------------------------------------------------------------- #
# Application
# --------------------------------------------------------------------------- #

application = webapp.WSGIApplication(
				      [('/', MainPage)],
				      debug=True)

def main():
  run_wsgi_app(application)
   
if __name__ == "__main__":
  main()