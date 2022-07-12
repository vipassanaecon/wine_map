#Importing and manipulating our data
#1 #import our data
import pandas as pd

df = pd.read_csv(r"C:\Users\straw\Desktop\wine_map\napa_wine_full.csv", encoding= 'unicode_escape')
df

#2 #creating our Map Address column
df['Map Address'] = df['Address'].astype(str) + ',' + \
                  df['City'] + ',' + 'CA'
df.head()

#3 #drop all P.O. box addresses
df_copy = df[df["Address"].str.contains("P.O. Box")==False].copy()
df = df_copy
df

#4 import geopy and Nominatim geocoding service
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Wine Map", timeout=10)

#5 #assign our geocode variable and use RateLimiter function
from geopy.extra.rate_limiter import RateLimiter

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

#6 create geocode Location column 
df['Location'] = df['Map Address'].apply(geocode) #takes about 13minutes
df.head()

#7 #drop all addresses listed as "None"
df_copy = df[df['Location'].notna()].copy()
df = df_copy
df

#8 #create “Point” column that lists longitude, latitude, and altitude
df['Point'] = df['Location'].apply(lambda loc: tuple(loc.point) if loc else None)
df.head()

#9 #split up the Point column
df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(df['Point'].tolist(), index=df.index)
df.head()

#10 import folium and create map
import folium

map = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.Marker(location=[row["Latitude"], row["Longitude"]], tooltip=row["Winery"]).add_to(map), axis=1)
map

#11 #alternative map version
map = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.CircleMarker(location=[row["Latitude"], row["Longitude"]], tooltip=row["Winery"], fill=True, color = 'red',  radius=1).add_to(map), axis=1)
map
