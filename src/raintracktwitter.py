#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import simplejson
import urllib
import re

from raintrack import Raintrack

# --------------------------------------------------------------------------- #
# RainTrack Twitter
# --------------------------------------------------------------------------- #

class RaintrackTwitter(Raintrack):
    
    # ----------------------------------------------------------------------- #
    # Constructor
    # ----------------------------------------------------------------------- #

    def __init__(self, query = '#raintrack'):
      self.query = query
      self.rest  = self.createREST()
    
    # ----------------------------------------------------------------------- #
    # createREST
    # ----------------------------------------------------------------------- #

    def createREST(self):
    
      # Idea: in the last N hours/days [does yql pre-limit 15 entries?]
      # from datetime import datetime
      # from datetime import timedelta
      # (datetime.utcnow() - timedelta(hours=6))
      #		.strftime("%a, %d %b %Y %H:%M:%S +0000")

      # YQL REST Query
      rest = {
	"url": "http://query.yahooapis.com/v1/public/yql",
	"fields": {
	  "q": "select * from twitter.search where q='" + self.query + "'", 
	      # Idea: and created_at > 'Sat, 20 Mar 2010 23:42:00 +0000'",
	  "format": "json",
	  "diagnostics": "false",
	  "env": "store://datatables.org/alltableswithkeys"
	}
      }
      
      return rest
    
    # ----------------------------------------------------------------------- #
    # getResults
    # ----------------------------------------------------------------------- #
    
    def getResults(self):
      
      # Perform Query
      try:
	response = urllib.urlopen(url  = self.rest['url'], 
				  data = urllib.urlencode(self.rest['fields']))
      except:
	return None
    
      # Parse Response into Results
      json = simplejson.load(response)
      
      # No results
      if not json['query']['results']:
	return None
	
      # Some results
      results = json['query']['results']['results']

      # John: clever guy (fixes 'limit 1')
      if type(results) != type([]):
	results = [results]

      # example: for result in results
      # 	self.response.out.write(result['created_at'] + '<br />')
      # 	self.response.out.write(result['text'] + '<br /><br />')

      # Return results
      return results
      
    # ----------------------------------------------------------------------- #
    # getPlaces
    # ----------------------------------------------------------------------- #

    def getPlaces(self):
      
      # Perform Query & Get Results
      results = self.getResults()
    
      if not results:
	return None
	
      # Parse Results into Places
      places = []
      for result in results:
	
	# Pattern: #raintrack comment @ address
	regex = re.match('^.raintrack (?P<comment>.*) @ (?P<address>.*)$', 
			 result['text'])
	
	if regex:
	  place = {
	    'comment': regex.group('comment'),
	    'address': regex.group('address')
	  }
	  
	  # New place
	  places.append(place)
	  
	  # Skip
	  continue
	
	# Pattern: #raintrack address
	regex = re.match('^.raintrack (?P<address>.*)$', 
			 result['text'])
	
	if regex:
	  place = {
	    'comment': '',
	    'address': regex.group('address')
	  }
      
	  # New place
	  places.append(place)
	  
      # Return places
      return places