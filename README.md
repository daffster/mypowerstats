mypowerstats
============
Retrieve information from the Eskom API

##What's going on here?
This code makes a query to the myeskom.co.za website and pulls out the publically available information.
Nothing funny is going on here, its just a different way to display the information that Eskom has made available

##Why?

I wanted something that displayed a simple 2-line summary. No fancy webapp, no icons. Just text

##Getting data thats relevant to you

You will need two pieces of information from the myeskom.co.za website in order for this to work.
To get these pieces of information:

1. Go to http://www.myeskom.co.za/
2. Register an account (click on the top left icon -> My profile)
3. Open your web browsers Developer console, go to the Network tab.
4. Go back to the dashboard (top left icon -> Dashboard)
5. Scroll through the Network requests, look for a **POST** to **24?=<numbers>**, Click it
6. Select the Params subtab
7. Copy the _authKey_ and _city_ values
8. Put _authKey_ and _city_ into the mypowerstats scripts in place of the bogus values


##What you'll get

The response from the myeskom site is a JSON Object.

In the object you'll find some useful things, and some useless things

Useful:
- 'status' = Power Alert Status (Eskom's colour index of grid status)
- 'level' = Power Level (Eskom's way of stating the grid load)
- 'levelstatus' = Power Trend (Trend of the load. Up/Down/Stable)

Sort of useful:
- 'location' = Location (incase you forgot)
- 'tmp' = Outside Temperature (Celcius)
- 'appliances' = An Array of Appliances that Eskom thinks you should turn off
  - 'name' = Name of the appliance you should turn off

Useless:
- 'nextloadsheddingdate' = Next Load Shedding Date (I've never seen this populated. It's always null)
- 'tiptitle' and 'tipofday' = Eskom gives you helpful Tips on saving electricity. Like using a blanket instead of a heater.

##Credits

Written and maintained by Kieran Murphy <daffy@daffy.za.net>

If you find this helpful in any way and you want to say thanks, feel free to donate Bitcoin at **1Eyr72dHQs3RCo1tpXDeccyxjzqyXdYvuH**

Thanks!



