#1
import pandas as pd

df = pd.read_csv(r"C:\Users\straw\vipassanaecon projects\Medium Articles\python_wine_examples\napa_wine_full.csv", encoding= 'unicode_escape')
df

#2
df['Map Address'] = df['Address'].astype(str) + ',' + \
                  df['City'] + ',' + 'CA'
df.head()

#3
df_copy = df[df["Address"].str.contains("P.O. Box")==False].copy()
df = df_copy
df

#4
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Wine Map", timeout=10)

#5
from geopy.extra.rate_limiter import RateLimiter

geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

#6
df['Location'] = df['Map Address'].apply(geocode) #takes about 13minutes
df.head()

#7
df_copy = df[df['Location'].notna()].copy()
df = df_copy
df

#8
df['Point'] = df['Location'].apply(lambda loc: tuple(loc.point) if loc else None)
df.head()

#9
df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(df['Point'].tolist(), index=df.index)
df.head()

#10
import folium

map = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.Marker(location=[row["Latitude"], row["Longitude"]]).add_to(map), axis=1)
map

#11
map = folium.Map(
    location=[38.297539, -122.286865],
    tiles='cartodbpositron',
    zoom_start=12,
)
df.apply(lambda row:folium.CircleMarker(location=[row["Latitude"], row["Longitude"]], tooltip=row["Winery"], fill=True, color = 'red',  radius=3).add_to(map), axis=1)
map
