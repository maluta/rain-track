from pymaps import *


if __name__ == "__main__":
    import sys
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
    
    open('test.htm','wb').write(g.showhtml())   # generate test file
