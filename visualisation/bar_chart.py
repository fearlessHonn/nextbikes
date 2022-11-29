import streamlit as st
import pandas as pd
from data.database import Database


def display():
    st.title('Duration of trips')

    # --- Get data ---
    db = Database(path='data/bike_data.db')
    num_of_trips = db.get_num_of_trips()
    bar_chart_data = db.group_trips_by_duration()
    bar_chart_data = pd.DataFrame(bar_chart_data, columns=['duration in minutes', 'percentage of trips'])

    # --- Split diagram @ 31 minutes ---
    first_part = bar_chart_data.iloc[:32]
    second_part = pd.DataFrame({'duration in minutes': 32, 'percentage of trips': sum(bar_chart_data.iloc[32:]['percentage of trips'])}, index=[32])

    data = pd.concat([first_part, second_part], ignore_index=False)

    # --- Plot diagram ---
    data['percentage of trips'] = [round(float(i) / num_of_trips * 100, 1) for i in data['percentage of trips']]
    st.bar_chart(data, y='percentage of trips', x='duration in minutes')