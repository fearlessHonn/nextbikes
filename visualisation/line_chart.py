import streamlit as st
import pandas as pd
import sys

sys.path.append('C:/Users/henlu/PycharmProjects/nextbikes/data')
from database import Database


def display():
    st.sidebar.header('Line Graph:')
    interval = st.sidebar.slider('Interval', 5, 60, 15, 5, '%i minutes') * 60

    st.title('Number of trips throughout the day')

    # --- Get data ---
    db = Database(path='data/bike_data.db')
    line_chart_data = db.trips_per_interval(interval)
    line_chart_data = pd.DataFrame(line_chart_data, columns=['trips', 'time'])

    # --- Plot diagram ---
    st.line_chart(line_chart_data, y='trips', x='time')