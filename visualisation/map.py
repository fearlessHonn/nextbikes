import pandas as pd
import sys
import streamlit as st
import pydeck as pdk
from route import get_dataframe
from style import map_styles, color1, color2

sys.path.append('C:/Users/henlu/PycharmProjects/nextbikes/data')
from database import Database


st.set_page_config(page_title='Nextbikes',
                   page_icon=':bike:',
                   layout='wide')

db = Database(path='../data/bike_data.db')

hex_radius = st.sidebar.slider('Select a radius for the hexagons', 1, 100, 10)

bike_ids = db.get_bike_ids()
query_bike_id = st.sidebar.selectbox('Select bike id:', [i[0] for i in bike_ids])

print(query_bike_id)
trips = db.get_trips_of_bike(query_bike_id)

routes = get_dataframe(trips[0])
for trip in trips[1:]:
    routes = routes.append(get_dataframe(trip, prev_id=len(routes)), ignore_index=True)

trips = pd.DataFrame(trips, columns=['bike_id', 'start_time', 'start_lat', 'start_lon', 'start_name', 'start_id', 'end_time', 'end_lat', 'end_lon', 'end_name', 'end_id'])
last_trip = trips.iloc[-1]
last_trip[2], last_trip[3] = last_trip[7], last_trip[8]
trips = trips.append(last_trip, ignore_index=True)


max_id = len(routes) - 1


GET_COLOR_JS = [
    f"{color1[0]} + {color2[0] - color2[0]} * (id / {max_id})",
    f"{color1[1]} + {color2[1] - color1[1]} * (id / {max_id})",
    f"{color1[2]} + {color2[2] - color1[2]} * (id / {max_id})"
    f"155 + 100 * (id / {max_id})"
]

st.sidebar.title('Layers:')
line_vis = 1 if st.sidebar.checkbox('Lines', value=True) else 0

map_style = st.sidebar.selectbox('Select Map Style:', ('Streets',
                                                       'Light',
                                                       'Dark',
                                                       'Satellite',
                                                       'Outdoors',
                                                       'Satellite Streets',
                                                       'Navigation Day',
                                                       'Navigation Night'))

line_layer = pdk.Layer(
    'LineLayer',
    data=routes,
    get_source_position='[start_lon, start_lat]',
    get_target_position='[end_lon, end_lat]',
    get_width=10,
    get_color=GET_COLOR_JS,
    pickable=True,
    picking_radius=250,
    opacity=line_vis,)

scatterplot_layer = pdk.Layer(
    'ScatterplotLayer',
    data=trips,
    get_position='[start_lon, start_lat]',
    get_radius=50,
    opacity=line_vis,
    get_fill_color=[22, 22, 22],
    pickable=False)

map_layers = [scatterplot_layer, line_layer]

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
    tooltip={"html": f"&#128690 {{bike_id}} <br> &#128197 {{start_time}} <br> &#128337 {{duration}} Minuten <br>  &#x2194  {{distance}} km", "style": {"color": "white"}}
))
