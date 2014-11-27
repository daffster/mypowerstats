#!/usr/bin/env python

from httplib2 import Http
from urllib import urlencode
import time
import json

h = Http()

# Get these values from the request to https://www.myeskom.co.za/pages/Dashboard/24
data = dict(authKey="repl4c3m3w1ths0m3th1ngl3g1t000", city="xxx")

headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'https://www.myeskom.co.za', 'Referer': 'https://www.myeskom.co.za/'}

# The timestamp should be GMT+2. So if you're running from outside of South Africa, you may need to adjust this
timestamp=str(int(time.time()*1000))
resp, content = h.request("https://www.myeskom.co.za/pages/Dashboard/24?v="+timestamp, "POST", headers=headers, body=urlencode(data))

object_response = json.loads(content)

# All the useful stuff is in data->page
powerinfo = object_response['data']['page']

print "Power Status:    %s/%s/%s" % (powerinfo['level'],powerinfo['levelstatus'],powerinfo['status'],)
try:
    print "Poweroff Amount: %s" % (powerinfo['possiblepoweroffamount'],)
except KeyError:
    pass
try:
    if powerinfo['nextloadsheddingdate']:
        # I've never seen them actually populate this field...
        print "Next Loadshedding:\t%s" % (powerinfo['nextloadsheddingdate'],)
except KeyError:
    pass
try:
    appliances = powerinfo['appliances']
    turnoff = [] 
    for appliance in appliances:
        turnoff.append(appliance['name'])
except KeyError:
    pass
print "Turn off:        %s" % (",".join(turnoff),)

# If you want to see what else is available, uncomment the below lines
#from pprint import pprint
#pprint(object_response)
