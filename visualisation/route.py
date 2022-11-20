import requests
import os
import pandas as pd
from datetime import datetime
import warnings
from time import sleep
import sqlite3

api_key = os.environ.get('ORS_API_KEY')
api_key = '5b3ce3597851110001cf62489cc33275fcde43b994eade7aeb105fbd'


def get_route(start_latitude, start_longitude, end_latitude, end_longitude):
    if (route := read_route(start_latitude, start_longitude, end_latitude, end_longitude)) is not False:
        return route

    sleep(1.5)
    url = 'https://api.openrouteservice.org/v2/directions/cycling-regular/geojson'
    headers = {'Authorization': api_key}
    data = {"coordinates": [[start_longitude, start_latitude], [end_longitude, end_latitude]]}

    route = requests.post(url, headers=headers, json=data).json()

    if 'error' in route.keys():
        if route['error'] == 'Rate limit exceeded':
            sleep(5)
            warnings.warn('Rate limit exceeded, waiting 5 seconds')
            return get_route(start_latitude, start_longitude, end_latitude, end_longitude)
        warnings.warn('Error in route generation!')
        return [], 0

    try:
        distance = route['features'][0]['properties']['summary']['distance']
    except KeyError:
        distance = 0
        warnings.warn('Error in route generation!')

    response = [(j, i) for i, j in route['features'][0]['geometry']['coordinates']], distance
    write_route(start_latitude, start_longitude, end_latitude, end_longitude, response)
    return response


def get_dataframe(trip, prev_id=0):
    start_latitude, start_longitude, end_latitude, end_longitude = trip[2], trip[3], trip[7], trip[8]
    route = get_route(start_latitude, start_longitude, end_latitude, end_longitude)
    duration = (datetime.strptime(trip[6], '%Y-%m-%d %H:%M:%S') - datetime.strptime(trip[1], '%Y-%m-%d %H:%M:%S')).seconds // 60
    df = pd.DataFrame([(a, b, c, d, e + prev_id, trip[0], datetime.strptime(trip[1], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y %H:%M'), duration, trip[4], trip[9], round(route[1] / 1000, 2)) for e, ((a, b), (c, d)) in enumerate(zip(route[0][:-1], route[0][1:]))], columns=['start_lat', 'start_lon', 'end_lat', 'end_lon', 'id', 'bike_id', 'start_time', 'duration', 'start_name', 'end_name', 'distance'])
    return df


def read_route(start_lat, start_lon, end_lat, end_lon):
    db_conn = sqlite3.connect(path + 'routes.db')
    cursor = db_conn.cursor()

    cursor.execute(f'SELECT * FROM routes WHERE start_lat={start_lat} AND start_lon={start_lon} AND end_lat={end_lat} AND end_lon={end_lon}')
    if (route := cursor.fetchone()) is not None:
        route_id = route[0]
        distance = route[-1]
    else:
        return False

    cursor.execute(f'SELECT latitude, longitude FROM coordinates WHERE route_id={route_id} ORDER BY coordinate_id ASC')
    coordinates = cursor.fetchall()
    return coordinates, distance


def write_route(start_lat, start_lon, end_lat, end_lon, response):
    db_conn = sqlite3.connect(path + 'routes.db')
    cursor = db_conn.cursor()

    cursor.execute("SELECT id FROM routes ORDER BY id DESC LIMIT 1")
    route_id = cursor.fetchone()
    if not route_id:
        route_id = 0
    else:
        route_id = route_id[0] + 1

    cursor.execute(f'INSERT INTO routes VALUES ({route_id}, {start_lat}, {start_lon}, {end_lat}, {end_lon}, {response[1]})')
    for i, (latitude, longitude) in enumerate(response[0]):
        cursor.execute(f'INSERT INTO coordinates VALUES ({route_id}, {latitude}, {longitude}, {i})')
    db_conn.commit()


if __name__ == '__main__':
    path = ''
    print(get_route(52.51861, 13.27698, 52.52861, 13.37698))

else:
    path = 'visualisation/'