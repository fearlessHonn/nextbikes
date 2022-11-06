class Dataset:
    def __init__(self, data):
        self.booked_bikes = data['booked_bikes']
        self.available_bikes = data['available_bikes']
        self.set_point_bikes = data['set_point_bikes']
        self.timestamp = data['timestamp']
        self.city_id = data['city_id']
