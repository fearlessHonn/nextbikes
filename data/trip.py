from location import Location


class Trip:
    def __init__(self, bike_id, start_time, start_location: Location, end_time, end_location: Location):
        self.start_time = start_time
        self.start_location = start_location
        self.end_time = end_time
        self.end_location = end_location

        self.bike_id = bike_id


    def __str__(self):
        return f"Start time: {self.start_time}, Start location: {self.start_location}, End time: {self.end_time}, End location: {self.end_location}, Bike_id: {self.bike_id}"