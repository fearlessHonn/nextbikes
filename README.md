# nextbikes

## Datenbank
Bei der Datenbank handelt es sich um eine sqlite3 Datenbank. 
### Trips

 1. bike_id: ID des Fahrrads, steht auch auf den Fahrrädern drauf - 5stellige Zahl
 --------------------------
 2. start_time: Zeitstempel in der Form: '%Y-%m-%d %H:%M:%S' als das Fahrrad das letzte Mal an dieser Stelle gesehen wurde
 3. start_lat: Breitengrad der Startposition
 4. start_lon: Längengrad der Startposition
 5. start_name: Name der Startposition (bei bekannten Stationen z.B. Hauptbahnhof - bei freistehenden Fahrrädern 'BIKE {bike_id}')
 ----------------------------
 6. end_time: Zeitstempel in der Form: '%Y-%m-%d %H:%M:%S' als das Fahrrad das erste Mal an dieser Stelle gesehen wurde
 7. end_lat: Breitengrad der Endposition
 8. end_lon: Längengrad der Endposition
 9. end_name: Name der Endposition (bei bekannten Stationen z.B. Hauptbahnhof - bei freistehenden Fahrrädern 'BIKE {bike_id}') 
 
 ### Datasets
 1. dataset_id: laufzeit generierte ID des datasets, jedes Mal um 1 inkrementiert
 2. city_id: ID der Stadt, zu der das dataset gehört (s. cities-table)
 3. booked_bikes:
 4. available_bikes:
 5. set_point_bikes:
 6. timestamp:
 
 ### Cities
 1. uid:
 2. name:
 3. latitude:
 4. longitude:
 5. num_places:
 6. return_to_official_only:
 7. website:
 
 ### Locations
 1. location_id:
 2. city_id:
 3. latitude:
 4. longitude:
 5. location_name:
 
