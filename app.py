import streamlit as st
from multiapp import MultiApp
from apps import (
    home, 
    indonesia,
    jakarta,
    world,
    predictions)

# SET UP PAGE
st.set_page_config(page_title='COVID-19 Dashboard',
                    page_icon=":bar_chart:",
                    layout="wide"
    )

app = MultiApp()

app.add_app("Home", home.app)
app.add_app("COVID-19: Indonesia", indonesia.app)
app.add_app("COVID-19: Jakarta", jakarta.app)
app.add_app("COVID-19: World", world.app)
app.add_app("COVID-19 in Indonesia: Forecast", predictions.app)


app.run()