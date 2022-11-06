import requests
import os
import pandas as pd
from datetime import datetime
import warnings

api_key = os.environ.get('ORS_API_KEY')


def get_route(start_latitude, start_longitude, end_latitude, end_longitude):
    url = 'https://api.openrouteservice.org/v2/directions/cycling-regular/geojson'
    print(api_key)
    headers = {'Authorization': api_key}
    data = {"coordinates": [[start_longitude, start_latitude], [end_longitude, end_latitude]]}

    route = requests.post(url, headers=headers, json=data).json()

    if 'error' in route.keys():
        warnings.warn('Error in route generation!')
        return [], 0

    try:
        distance = route['features'][0]['properties']['summary']['distance']
    except KeyError:
        distance = 0
    return [(j, i) for i, j in route['features'][0]['geometry']['coordinates']], distance


def get_dataframe(trip, prev_id=0):
    start_latitude, start_longitude, end_latitude, end_longitude = trip[2], trip[3], trip[7], trip[8]
    route = get_route(start_latitude, start_longitude, end_latitude, end_longitude)
    df = pd.DataFrame([(a, b, c, d, e + prev_id, trip[0], datetime.strptime(trip[1], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y %H:%M'), (datetime.strptime(trip[1], '%Y-%m-%d %H:%M:%S') - datetime.strptime(trip[6], '%Y-%m-%d %H:%M:%S')).seconds // 3600, trip[4], trip[9], round(route[1] / 1000, 2)) for e, ((a, b), (c, d)) in enumerate(zip(route[0][:-1], route[0][1:]))], columns=['start_lat', 'start_lon', 'end_lat', 'end_lon', 'id', 'bike_id', 'start_time', 'duration', 'start_name', 'end_name', 'distance'])

    return df

