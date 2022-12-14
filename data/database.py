import sqlite3
import warnings
from data.dataset import Dataset
from data.location import Location
from data.trip import Trip


class Database:
    def __init__(self, path='bike_data.db'):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def new_city(self, data):
        self.cursor.execute(f"SELECT uid FROM cities WHERE uid = {data['uid']}")
        if not self.cursor.fetchone():
            self.cursor.execute(
                f""" INSERT INTO cities VALUES ("""
                f""" {data['uid']}, '{data['name']}', {data['lat']}, {data['lng']},"""
                f""" {data['num_places']}, {data['return_to_official_only']}, '{data['website']}')""")
            self.conn.commit()

    def new_location(self, location: Location, city_id: int):
        self.cursor.execute(f"SELECT location_id FROM locations WHERE location_id = {location.uid}")
        if not self.cursor.fetchone():
            self.cursor.execute(
                f"""INSERT INTO locations VALUES 
                ({location.uid},
                {city_id},
                {location.lat},
                {location.lng},
                '{location.name}')""")
            self.conn.commit()

    def new_dataset(self, dataset: Dataset) -> int:
        self.cursor.execute("SELECT dataset_id FROM datasets ORDER BY dataset_id DESC LIMIT 1")
        dataset_id = self.cursor.fetchone()
        if not dataset_id:
            dataset_id = 0
        else:
            dataset_id = dataset_id[0] + 1
        self.cursor.execute(
            f"""INSERT INTO datasets VALUES ({dataset_id}, {dataset.city_id}, {dataset.booked_bikes}, {dataset.available_bikes}, {dataset.set_point_bikes}, {dataset.timestamp})""")
        self.conn.commit()
        return dataset_id

    def new_trip(self, trip: Trip):
        print(trip)
        self.cursor.execute(
            f"""INSERT INTO trips VALUES 
                ({trip.bike_id}, 
                {trip.start_time}, {trip.start_location.lat}, {trip.start_location.lng}, '{trip.start_location.name}', {trip.start_location.uid}, 
                {trip.end_time}, {trip.end_location.lat}, {trip.end_location.lng}, '{trip.end_location.name}', {trip.end_location.uid})""")

        self.conn.commit()

    def get_bike_ids(self):
        self.cursor.execute(f"SELECT bike_id FROM trips GROUP BY bike_id ORDER BY count(*)")
        return self.cursor.fetchall()

    def trips_per_interval(self, interval: int):
        self.cursor.execute(f"SELECT count(*), STRFTIME('%H:%M', start_time) from trips GROUP BY cast(STRFTIME('%s', start_time) / {interval} as int) * {interval}")
        return self.cursor.fetchall()

    def get_trips_of_bike(self, bike_id: int):
        self.cursor.execute(f"SELECT * FROM trips WHERE bike_id = {bike_id}")
        return self.cursor.fetchall()

    def group_trips_by_duration(self):
        self.cursor.execute("SELECT (STRFTIME('%s', end_time) - STRFTIME('%s', start_time)) / 60, count(*) FROM trips GROUP BY (STRFTIME('%s', end_time) - STRFTIME('%s', start_time)) / 60;")
        return self.cursor.fetchall()

    def get_num_of_trips(self):
        self.cursor.execute("SELECT count(*) FROM trips")
        return self.cursor.fetchone()[0]

    def get_all_trips(self):
        self.cursor.execute("SELECT start_lat, start_lon FROM trips")
        return self.cursor.fetchall()
