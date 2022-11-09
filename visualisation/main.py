import streamlit as st
import map
import bar_chart
import line_chart

st.set_page_config(page_title='Nextbikes',
                   page_icon=':bike:',
                   layout='wide')

st.title('Nextbike Visualisation')

st.sidebar.title('Settings')

map.display()
line_chart.display()
bar_chart.display()