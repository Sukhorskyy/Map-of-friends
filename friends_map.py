import json
import pandas
import folium
import twitter2
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


def read_data(path):
    '''
    Return data from .json file
    '''
    with open(path, mode='r', encoding='utf-8') as friend_file:
        data = json.load(friend_file)
    return data


def get_frinds(data):
    '''
    Return DataFrame of 5 friends with their coordinates
    '''
    data = data['users']
    friend_list = []
    for user in data:
        name = user['name']
        location = user['location']
        if location != '':
            friend_list.append([name, location])
    df = pandas.DataFrame(friend_list, columns = ['Name', 'Location'])
    
    locator = Nominatim(user_agent='myGeocoder', timeout=None)
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    df['exact_loc'] = df['Location'].apply(geocode)
    df['point'] = df['exact_loc'].apply(lambda loc: tuple(loc.point) if loc else None)
    df[['latitude', 'longitude', 'altitude']] = pandas.DataFrame(df['point'].tolist(), index=df.index)
    del df['point']
    del df['altitude']
    df = df.dropna()

    return df


def create_map(friends):
    '''
    Create map using DataFrame
    '''
    lat = friends['latitude']
    lon = friends['longitude']
    name = friends['Name']
    map = folium.Map(location=[48.8566, 2.3522], zoom_start=3, control_scale=True)
    fg = folium.FeatureGroup(name='map', )
    for lt, ln, nm in zip(lat, lon, name):
        fg.add_child(folium.Marker(location=[lt, ln], \
            popup=nm, icon=folium.Icon(color="red", icon="user")))
    map.add_child(fg)
    map.save('templates\index.html')


def main(user):
    user_data = twitter2.result(user)
    with open('user_data.json', mode='w', encoding='utf-8') as data_file:
        json.dump(user_data, data_file, indent=4)
    create_map(get_frinds(read_data('user_data.json')))