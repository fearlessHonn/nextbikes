from location import Location, default_location
from trip import Trip
from timestamp import Timestamp
from database import Database
from dataset import Dataset
import requests
import datetime
import warnings
from collections import defaultdict



class City:
    def __init__(self, name: str):
        self.name = name
        self.database = Database('bike_data.db')

        try:
            data = requests.get('https://api.nextbike.net/maps/nextbike-official.json?countries=de').json()
            self.uid = \
                [city for provider in data['countries'] for city in provider['cities'] if city['name'] == name][0][
                    'uid']

        except IndexError:
            raise IndexError(f'City "{name}" not found')

        data = requests.get(f'https://api.nextbike.net/maps/nextbike-live.json?city={self.uid}').json()['countries'][0][
            'cities'][0]
        city_data_keys = ['uid', 'name', 'lat', 'lng', 'num_places', 'return_to_official_only', 'website']
        city_data = {key: data[key] for key in city_data_keys}
        self.database.new_city(city_data)

        self.current_dataset = None
        self.current_places = dict()

        self.bikes_last_seen = dict() # int: (Location, Timestamp)

        self.locations = []
        self.seen_locations = []
        self.bikes = {}
        self.current_dataset_id = 0
        self.refresh()

        self.lat = data['lat']
        self.lng = data['lng']

    def refresh(self) -> bool:
        url = f'https://api.nextbike.net/maps/nextbike-live.json?city={self.uid}'
        try:
            data = requests.get(url).json()['countries'][0]['cities'][0]
        except requests.exceptions.ConnectionError:
            print('No Connection possible')
            return False

        timestamp_keys = ['booked_bikes', 'available_bikes', 'set_point_bikes']
        timestamp = datetime.datetime.now().strftime("'%Y-%m-%d %H:%M:%S'")
        timestamp_object = Timestamp(timestamp)

        self.current_dataset = Dataset({'timestamp': timestamp, **{key: data[key] for key in timestamp_keys}, 'city_id': self.uid})
        timestamp_object.dataset_id = self.database.new_dataset(self.current_dataset)

        self.current_places = data['places']
        current_bike_locations = dict()
        for place in self.current_places:
            location = Location(place['uid'], place['name'], place['lat'], place['lng'])

            if place['spot']:
                self.database.new_location(location, self.uid)

            bikes_at_location = place['bike_numbers']
            current_bike_locations.update({bike: (location, timestamp_object) for bike in bikes_at_location})

        for bike, (location, timestamp_object) in current_bike_locations.items():
            try:
                if self.bikes_last_seen[bike][1].dataset_id != timestamp_object.dataset_id - 1:
                    trip = Trip(bike, self.bikes_last_seen[bike][1].timestamp, self.bikes_last_seen[bike][0], timestamp, location)
                    self.database.new_trip(trip)
            except KeyError:
                warnings.warn(f'Bike {bike} not found in dict.')

        self.bikes_last_seen.update(current_bike_locations)

        return True