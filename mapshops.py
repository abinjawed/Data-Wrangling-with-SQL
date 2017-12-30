"""
Created on Mon Dec 18 22:17:20 2017

@author: awadbin-jawed
"""
#pip install geocoder
import gmplot
import pandas as pd
import geocoder

count=10
names=['Facility Street Number','Facility Pre-Direction','Facility Street Name','Facility Street Type', 'Facility Unit Number','Facility City','	Facility Zip Code']

df = pd.read_csv('shops.csv')
df=df.fillna("")
#df['address']=df[names[0]]+', '+df[[7]]+', '+df[[8]]+', '+df[[9]]+', '+df[[10]]+', '+df[[11]]+', '+df[[12]].astype(str)
df['address']=df[names[0]].astype(str)+', '+df[names[1]]+', '+df[names[2]]+', '+df[names[3]]+', '+df[names[4]]+', '+df[names[5]]+', '+df['Facility Zip Code'].astype(str)
df.head()


#g = geocoder.google('543, N, BRYANT, ST,DENVER, 80204')
#g.latlng
address=df['address']
ids=df['Business File Number']


gmap = gmplot.GoogleMapPlotter.from_geocode("Denver")



lats = []
lons = []
titles = []
k=0
i=0
while(k<11):
    g = geocoder.google(address[i])
    c=g.latlng
    print(c)
    if(c != None):
    #gmap_coord = get_coord(c)
        lats.append(c[0])
        lons.append(c[1])
        titles.append(ids[i])
        k+=1
    i+=1

#add points to map
gmap.scatter(lats[0:k-1], lons[0:k-1], 'green', size=100, marker=False)

for i in range(k):
    gmap.marker(lats[i], lons[i], title=titles[i])
#save to map
gmap.draw("mapShop.html")
