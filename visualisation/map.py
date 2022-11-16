import pydeck as pdk
from visualisation.route import get_dataframe
from visualisation.style import map_styles, get_color
import pandas as pd
import streamlit as st

import sys
sys.path.append('C:/Users/henlu/PycharmProjects/nextbikes/data')
from database import Database


def display():
    db = Database(path='data/bike_data.db')

    bike_ids = db.get_bike_ids()
    st.sidebar.header('Map')
    query_bike_id = st.sidebar.selectbox('Select bike id:', [i[0] for i in bike_ids])

    trips = db.get_trips_of_bike(query_bike_id)

    routes = get_dataframe(trips[0])
    for trip in trips[1:]:
        routes = pd.concat([routes, get_dataframe(trip, prev_id=len(routes))], ignore_index=True)

    columns = ['bike_id', 'start_time', 'start_lat', 'start_lon', 'start_name', 'start_id', 'end_time',
               'end_lat', 'end_lon', 'end_name', 'end_id']
    trips = pd.DataFrame(trips, columns=columns)

    last_trip = trips.iloc[-1]
    last_trip = [v for i, v in last_trip.items()]
    last_trip[2], last_trip[3] = last_trip[7], last_trip[8]
    trips.loc[len(trips)] = last_trip
    trips['id'] = list(range(len(trips)))

    max_id = len(routes) - 1

    # --- Sidebar ---

    st.sidebar.subheader('Layers:')

    line_vis = 1 if st.sidebar.checkbox('Lines', value=False) else 0
    hex_vis = 1 if st.sidebar.checkbox('Hexagons', value=False) else 0
    heat_vis = 0.7 if st.sidebar.checkbox('Heatmap', value=True) else 0

    if hex_vis:
        st.sidebar.subheader('Hexagons:')
        hex_radius = st.sidebar.slider('Select a radius for the hexagons', 1, 100, 10)
    else:
        hex_radius = 0

    map_style = st.sidebar.selectbox('Select Map Style:', list(map_styles.keys()), index=3)

    line_layer = pdk.Layer(
        'LineLayer',
        data=routes,
        get_source_position='[start_lon, start_lat]',
        get_target_position='[end_lon, end_lat]',
        get_width=10,
        get_color=get_color(max_id),
        pickable=True,
        picking_radius=250,
        opacity=line_vis)

    scatterplot_layer = pdk.Layer(
        'ScatterplotLayer',
        data=trips,
        get_position='[start_lon, start_lat]',
        get_radius=20,
        opacity=line_vis,
        get_fill_color=[22, 22, 22],
        pickable=False)

    # --- Hexagon Layer ---

    all_trips = db.get_all_trips()
    all_trips = pd.DataFrame(all_trips, columns=['latitude', 'longitude'])

    hexagon_layer = pdk.Layer(
        'HexagonLayer',
        data=all_trips,
        get_position='[longitude, latitude]',
        radius=hex_radius,
        elevation_scale=4,
        elevation_range=[0, 1000],
        extruded=True,
        opacity=hex_vis)

    # --- Heatmap Layer ---

    heatmap_layer = pdk.Layer(
        'HeatmapLayer',
        data=all_trips,
        get_position='[longitude, latitude]',
        threshold=0.05,
        aggregation='MEAN',
        weights_texture_size=512,
        radius_pixels=50,
        opacity=heat_vis)

    map_layers = [heatmap_layer, hexagon_layer, scatterplot_layer, line_layer]

    tooltip = {
        "html": f"&#128690 {{bike_id}} <br> &#128197 {{start_time}} <br> &#128337 {{duration}} Minuten <br>  &#x2194  {{distance}} km",
        "style": {"color": "white", "border-radius": "6px", "border-style:": "solid", "border-width": "1px",
                  "opacity": "0.95"}}

    st.pydeck_chart(pdk.Deck(
        map_style=map_styles[map_style],
        initial_view_state=pdk.ViewState(
            latitude=routes.start_lat[0],
            longitude=routes.start_lon[0],
            zoom=11,
            pitch=50,
            pickable=True,
        ),
        layers=map_layers,
        tooltip=tooltip))