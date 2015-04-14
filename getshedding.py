#!/usr/bin/env python

# This script is provided with no documentation other than the comments contained within.
# I might change this, but due to demand I'm releasing without documentation for now.

from httplib2 import Http
from urllib import urlencode
import time
from datetime import datetime
from pytz import timezone
import json

def GetLoadsheddingStage():
    """ Return the current Loadshedding Stage
    0 = No load shedding
    1-3 = Stage 1-3
    """
    h = Http()
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 
            'Referer': 'https://loadshedding.eskom.co.za/', 
            'X-Requested-With': 'XMLHttpRequest'
            }

    timestamp=str(int(time.time()*1000))
    resp, content = h.request("http://loadshedding.eskom.co.za/LoadShedding/GetStatus?_="+timestamp, "GET", headers=headers)

    # Eskom responds with a single number
    # 1 = No load shedding
    # 2 = Stage 1
    # 3 = Stage 2
    # 4 = Stage 3
    response = {}
    if int(resp['status']) == 200:
        response['status'] = 'Success'
        response['stage'] = int(content)-1
    else:
        response['status'] = 'Error'
    return response

def GetLoadsheddingSchedule(supplier,suburb,stage):
    """ Retrieve the next Loadshedding based on suburb and loadshedding stage
    Currently only works for Johannesburg City Power
    supplier values:
    1 = Johannesburg City Power
    """
    if supplier == 1:
        h = Http()
        headers = {'Accept': '*/*', 'Referer': 'https://www.citypower.co.za/customers/Pages/Load_Shedding.aspx', 'Content-Type': 'application/json; charset=utf-8'}

        resp, content = h.request("https://www.citypower.co.za/LoadSheddingSchedule.axd?Suburb="+str(suburb)+"&Stage=Stage"+str(stage), "GET", headers=headers)

    response = {}
    if int(resp['status']) == 200:
        response['status'] = 'Success'
        response['events'] = json.loads(content)
    else:
        response['status'] = 'Error'
    return response

def GetNextLoadsheddingEvent(supplier,suburb,stage):
    """ Get the next Loadshedding Event for the supplied suburb
    """
    events = TidyCityPowerEvents(GetLoadsheddingSchedule(supplier,suburb,stage))
    timestamp=int(time.time())
    for event in events:
        if int(event['StartTimestamp']) < timestamp:
            #print "%s < %s" % (event['StartTimestamp'], timestamp,)
            pass
        else:
            return event
    return None

def TidyCityPowerEvents(events):
    """ City Power returns some rubbish in their events
    Lets clean it up to make our lives easier
    """
    TidiedEvents=[]
    if events['status'] == 'Success':
        for event in events['events']:
            tidy={}
            tidy['StartDate'] = datetime.fromtimestamp(int(event['StartDate'][6:-2])/1000, timezone('Africa/Johannesburg'))
            tidy['StartTimestamp'] = int(event['StartDate'][6:-2])/1000
            tidy['EndDate'] = datetime.fromtimestamp(int(event['EndDate'][6:-2])/1000, timezone('Africa/Johannesburg'))
            tidy['EndTimestamp'] = int(event['EndDate'][6:-2])/1000
            tidy['Title'] = event['Title']
            tidy['SubBlock'] = event['SubBlock']
            tidy['Suburb'] = event['Suburb']
            TidiedEvents.append(tidy)
        return TidiedEvents
    else:
        return None


# You need to find your Suburb from the citypower website.
suburb='244-4B'
print "Load Shedding Stage:    %s" % (GetLoadsheddingStage()['stage'],)
print GetNextLoadsheddingEvent(1,suburb,GetLoadsheddingStage()['stage'])
