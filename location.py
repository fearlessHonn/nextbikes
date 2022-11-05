class Location:
    def __init__(self, uid, name, lat, lng, **kwargs):
        self.lat = lat
        self.lng = lng
        self.uid = uid
        self.name = name
        self.type = kwargs.get('type', None)

    def __str__(self):
        return f"Location name: {self.name}, Latitude: {self.lat}, Longitude: {self.lng}, id: {self.uid}"


default_location = Location(0, 'Default', 0, 0, kwargs={'type': 'default'})
