import streamlit as st
from visualisation import map, bar_chart, line_chart

st.set_page_config(page_title='Nextbikes',
                   page_icon=':bike:',
                   layout='wide')

st.title('Nextbike Visualisation')

st.sidebar.title('Settings')

map.display()
line_chart.display()
bar_chart.display()