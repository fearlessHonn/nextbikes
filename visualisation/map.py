import pandas as pd
import sys
import streamlit as st
import pydeck as pdk
from route import get_dataframe
from datetime import datetime
sys.path.append('C:/Users/henlu/PycharmProjects/nextbikes/data')
from database import Database


st.set_page_config(page_title='Nextbikes',
                   page_icon=':bike:',
                   layout='wide')

db = Database(path='../data/bike_data.db')

trips = db.get_trips_of_bike(54303)

df = get_dataframe(trips[0])
for trip in trips[1:]:
    df = df.append(get_dataframe(trip, prev_id=len(df)), ignore_index=True)

max_id = len(df) - 1

color1 = [211, 83, 12]  # D38312
color2 = [168, 32, 79]  # A83279

GET_COLOR_JS = [
    f"{color1[0]} + {color2[0] - color2[0]} * (id / {max_id})",
    f"{color1[1]} + {color2[1] - color1[1]} * (id / {max_id})",
    f"{color1[2]} + {color2[2] - color1[2]} * (id / {max_id})"
    f"155 + 100 * (id / {max_id})"
]


line_layer = pdk.Layer(
    'LineLayer',
    data=df,
    get_source_position='[start_lon, start_lat]',
    get_target_position='[end_lon, end_lat]',
    get_width=10,
    get_color=GET_COLOR_JS,
    pickable=True,
    picking_radius=250)

map_layers = [line_layer]

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=df.start_lat[0],
        longitude=df.start_lon[0],
        zoom=11,
        pitch=50,
        pickable=True,
    ),
    layers=map_layers,
    tooltip={"html": f"&#128690 {{bike_id}} <br> &#128197 {{start_time}} <br> &#128337 {{duration}} Minuten <br>  &#x2194  {{distance}} km", "style": {"color": "white"}}
))
