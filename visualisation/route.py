import requests
import os
import pandas as pd

api_key = os.environ.get('ORS_API_KEY')
api_key = '5b3ce3597851110001cf62489cc33275fcde43b994eade7aeb105fbd'


def get_waypoints(start_latitude, start_longitude, end_latitude, end_longitude):
    url = 'https://api.openrouteservice.org/v2/directions/cycling-regular/geojson'
    print(api_key)
    headers = {'Authorization': api_key}
    data = {"coordinates": [[start_longitude, start_latitude], [end_longitude, end_latitude]]}

    route = requests.post(url, headers=headers, json=data).json()
    if 'error' in route.keys():
        return route['error']
    return [(j, i) for i, j in route['features'][0]['geometry']['coordinates']]


def get_dataframe(start_latitude, start_longitude, end_latitude, end_longitude, prev_id=0):
    waypoints = get_waypoints(start_latitude, start_longitude, end_latitude, end_longitude)
    df = pd.DataFrame([(a, b, c, d, e + prev_id) for e, ((a, b), (c, d)) in enumerate(zip(waypoints[:-1], waypoints[1:]))], columns=['start_lat', 'start_lon', 'end_lat', 'end_lon', 'id'])

    return df


print(get_dataframe(48.994617, 8.400361, 48.988131, 8.379993))
