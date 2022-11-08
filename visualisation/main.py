import pandas as pd
import sys
import streamlit as st
import pydeck as pdk
from route import get_dataframe
from style import map_styles, color1, color2
from datetime import datetime, timedelta

sys.path.append('C:/Users/henlu/PycharmProjects/nextbikes/data')
from database import Database

st.set_page_config(page_title='Nextbikes',
                   page_icon=':bike:',
                   layout='wide')

db = Database(path='../data/bike_data.db')

hex_radius = st.sidebar.slider('Select a radius for the hexagons', 1, 100, 10)

bike_ids = db.get_bike_ids()
query_bike_id = st.sidebar.selectbox('Select bike id:', [i[0] for i in bike_ids])

trips = db.get_trips_of_bike(query_bike_id)

routes = get_dataframe(trips[0])
for trip in trips[1:]:
    routes = pd.concat([routes, get_dataframe(trip, prev_id=len(routes))], ignore_index=True)

columns = ['bike_id', 'start_time', 'start_lat', 'start_lon', 'start_name', 'start_id', 'end_time',
                              'end_lat', 'end_lon', 'end_name', 'end_id']
trips = pd.DataFrame(trips, columns=columns)


last_trip: pd.Series = trips.iloc[-1]
last_trip.swa
trips = pd.concat([trips, pd.DataFrame(last_trip, columns=columns)], ignore_index=True)
trips['id'] = list(range(len(trips)))

max_id = len(routes) - 1


GET_COLOR_JS = [
    f"{color1[0]} + {color2[0] - color2[0]} * (id / {max_id})",
    f"{color1[1]} + {color2[1] - color1[1]} * (id / {max_id})",
    f"{color1[2]} + {color2[2] - color1[2]} * (id / {max_id})"
    f"155 + 100 * (id / {max_id})"
]

st.sidebar.title('Layers:')

line_vis = 1 if st.sidebar.checkbox('Lines', value=True) else 0

comment = """
min_date = datetime.strptime(routes['start_time'].min(), '%d.%m.%y %H:%M')
max_date = datetime.strptime(routes['start_time'].max(), '%d.%m.%y %H:%M')
if max_date != min_date:
    timeslot = st.sidebar.slider('See trips from', min_value=min_date, max_value=max_date, value=(min_date, max_date), format='DD.MM.YY HH:MM', step=timedelta(hours=3))
else:
    timeslot = (min_date, max_date)


filter_mask = (timeslot[1].strftime('%d.%m.%y %H:%M') >= routes['start_time']) & (routes['start_time'] >= timeslot[0].strftime('%d.%m.%y %H:%M'))
routes = routes[filter_mask]
"""

map_style = st.sidebar.selectbox('Select Map Style:', ('Streets',
                                                       'Light',
                                                       'Dark',
                                                       'Satellite',
                                                       'Outdoors',
                                                       'Satellite Streets',
                                                       'Navigation Day',
                                                       'Navigation Night'))

st.sidebar.title('Line Graph:')
interval = st.sidebar.slider('Interval', 5, 60, 15, 5, '%i minutes') * 60

line_layer = pdk.Layer(
    'LineLayer',
    data=routes,
    get_source_position='[start_lon, start_lat]',
    get_target_position='[end_lon, end_lat]',
    get_width=10,
    get_color=GET_COLOR_JS,
    pickable=True,
    picking_radius=250,
    opacity=line_vis, )

scatterplot_layer = pdk.Layer(
    'ScatterplotLayer',
    data=trips,
    get_position='[start_lon, start_lat]',
    get_radius=20,
    opacity=line_vis,
    get_fill_color=[22, 22, 22],
    pickable=False)

text_layer = pdk.Layer(
    'TextLayer',
    data=trips,
    get_position='[start_lon, start_lat]',
    get_text='id',
    get_size=300,
    getTextAnchor='"middle"',
    get_alignment_baseline='"bottom"')

map_layers = [text_layer, scatterplot_layer, line_layer]

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

chart_data = db.trips_per_interval(interval)

chart_data = pd.DataFrame(chart_data, columns=['trips', 'time'])
st.line_chart(chart_data, y='trips', x='time')
