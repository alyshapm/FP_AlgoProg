import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import altair as alt
import pydeck as pdk

# SET UP PAGE
st.set_page_config(page_title='COVID-19 Dashboard',
                    page_icon=":bar_chart:",
                    layout="wide"
)

# FETCHING DATA
DATE_TIME = "date/time"

def load_data():
    data = pd.read_csv(
        "covid_province.csv", 
        nrows=35)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis="columns", inplace=True)
    # data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data

data = load_data()

# # SIDEBAR
# st.sidebar.header("Please filter here:")

# MAP

def map(data, lat, long, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": long,
            "zoom": zoom,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["long","lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            )
        ]
    ))

row1_1, row1_2 = st.columns((2,3))

with row1_1:
    st.title("COVID-19 in Indonesia")
    # month_slct = st.slider("Select month", ) need to fix date format in csv

with row1_2:
    st.write()
