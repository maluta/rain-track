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

class MainHandler(webapp.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    q = [-23.58992, -46.66208, 'chuva forte']
    r = [-23.58970, -46.66288, 'chuva fraca']
    s = [-23.58920, -46.66328, 'sem chuva']

    key = "ABQIAAAALaTde9gMqHnzLPW58lcFTBRVCP9UC649_MmcUms9CnYxhjIH6hSvAPhEnL5l4nj4RN0QcnwWguiPIg" # you will get your own key
    
    g = PyMap(key)                         # creates an icon & map by default
    icon2 = Icon('icon2')               # create an additional icon
    icon2.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png" # for testing only!
    icon2.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png" # do not hotlink from your web page!
    g.addicon(icon2)
    
    g.maps[0].zoom = 15
    
    g.maps[0].setpoint(q)               # add the points to the map
    g.maps[0].setpoint(r)
    g.maps[0].setpoint(s)
    
#    open('test.htm','wb').write(g.showhtml())   # generate test file
    self.response.out.write(g.showhtml())   
    
    # generate test file




def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
