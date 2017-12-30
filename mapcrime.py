# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:12:24 2017

@author: a1
"""
#pip install gmplot
#pip install --upgrade gmplot
import gmplot

count=10
def get_coords():
    infile = open('crime.csv', 'r', encoding='utf-8')

    lats = []
    lons = []
    titles = []
    first_line = infile.readline()
    lines = infile.readlines()
    for line in lines:
        fields=line.split(",")
        lat=fields[13].replace("'","").replace('"', '').strip()
        lon=fields[12].replace("'","").replace('"', '').strip()
        #print(lon)
        if(lat !="" and lon!=""):
            lats.append(float(lat))
            lons.append(float(lon))
            titles.append(fields[0].replace("'","").replace('"', '').strip())
    return lats,lons,titles


lats,lons,titles=get_coords()
#count=len(lats)

#define the map starting
#gmap = gmplot.GoogleMapPlotter(lats[0],lons[0],15)
gmap = gmplot.GoogleMapPlotter.from_geocode("Denver")
#add points to map

gmap.scatter(lats[0:count], lons[0:count], 'red', size=100, marker=True)

for i in range(count+1):
    gmap.marker(lats[i], lons[i], title=titles[i])

#save to map
gmap.draw("mapCrime.html")
