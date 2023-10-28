import json
from math import sin, cos, sqrt, atan2, radians

#set the following and run it:
min_dist = 50.0
max_dist = 70.0
search_state = "Wisconsin" #set if you want to export a list of airports by state
distance_from = "KOSH"
print_all = True #print to console?

#leave these alone
R = 6373.0 #earth radius in kilometers, don't change
distance_from_lat = 0
distance_from_lon = 0
found_airports = []
num_of = 0

#function to calculate distance between two sets of coordinates, then convert to nautical miles
def calculate_distance(x,y):
    lat1 = radians(distance_from_lat)
    lon1 = radians(distance_from_lon)
    lat2 = radians(x)
    lon2 = radians(y)    
    dlon = lon2-lon1
    dlat = lat2-lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    return int(R*c*0.539957) #convert from km to nm, round off decimals

#import airport list from https://github.com/mwgg/Airports
with open('airports.json') as old_file: 
    d = json.load(old_file)

#find provided airport coordinates
for a in d:
    if(d[a]['icao'] == distance_from):
        distance_from_lat = d[a]['lat']
        distance_from_lon = d[a]['lon']

#loop through, find airports in provided state param and calculate distance from given airport
for a in d:
    if(d[a]['state'] == search_state or not search_state):
        dist = calculate_distance(d[a]["lat"],d[a]["lon"])
        if (dist <= max_dist and dist >= min_dist):
            d[a]["distance_from_airport"] = distance_from
            d[a]["distance_from_nm"] = dist
            found_airports.append(d[a])
            num_of += 1

#sort list by distance from origin
found_airports = sorted(found_airports, key=lambda airport: airport["distance_from_nm"])

#export found airports to file
if search_state:
    filename = search_state + '_airports.json'
else:
    filename = "airports_near_" + distance_from + ".json"
with open(filename,'w') as new_file:
    json.dump(found_airports, new_file, indent=2)

#print results to console
if (print_all):
    for a in found_airports:
        print(a["icao"], "-", a["name"], "-", a["distance_from_nm"], "nm miles from", distance_from)

print('min dist:',min_dist,', max_dist:',max_dist,', distance_from:',distance_from,', search_state:',search_state)
print(num_of,'results returned')
