#napa_wine_map 2.21.2022

#1
#import needed packages and assign variable geolocator
import pandas as pd
from geopy.geocoders import Nominatim

#Nominatim & OpenStreetMap
geolocator = Nominatim(user_agent="wine mapping app", timeout=100000)

#2
#import data into dataframe
df = pd.read_csv(r"C:\Users\straw\vipassanaecon projects\Medium Articles\python_wine_examples\napa_wine_full.csv",encoding= 'unicode_escape')
df

#3
#create concatenated map_address column that can be used with geocode function
df['map_address'] = df['Address'].astype(str) + ',' + \
                  df['City'] + ',' + 'CA'
df.head()

#4
#drop P.O. Box addresses and assign dataframe to new copy variable
#this will drop number of rows from 801 to 750 rows
#we will need to use .copy() when filtering original dataframes
#this is absolutely needed in order for process to work.
#https://stackoverflow.com/questions/32573452/settingwithcopywarning-even-when-using-locrow-indexer-col-indexer-value

new_df_copy = df[df["Address"].str.contains("P.O. Box")==False].copy() # drop P.O. Box addresses
df = new_df_copy
df

#5
from geopy.extra.rate_limiter import RateLimiter
# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

#6
# create location column that determines which addresses can be geocoded and which cannot
# some addresses cannot be geocoded (for unknown reason)
# 2- - create location column
df['location'] = df['map_address'].apply(geocode)

#7
# create point column that lists latitude and longitude, altitude coordinates
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

#8
#drop locations that cannot be geocoded
new_df_copy = df[df['point'].notna()].copy() #drop none locations
df = new_df_copy
df

#9
# split point columns into three seperate columns for folium to use
# 4 - split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

#10
#import mapping package: folium and create map
import folium

map1 = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.Marker(location=[row["latitude"], row["longitude"]]).add_to(map1), axis=1)
map1

#11
#other examples
#another example 1
map1 = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.Marker(location=[row["latitude"], row["longitude"]], popup='Custom Marker 1',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',icon='none')).add_to(map1), axis=1)
map1

#another example 2
wine_map = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=1).add_to(wine_map), axis=1)

wine_map
