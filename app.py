import streamlit as st
from multiapp import MultiApp
# import pages
from apps import (
    home, 
    indonesia,
    jakarta,
    world,
    predictions)

# set up page layout
st.set_page_config(page_title='COVID-19 Dashboard',
                    page_icon=":bar_chart:",
                    layout="wide"
    )

# declare instance of the app
app = MultiApp()

# add new up using the class function add_app, which takes title and func as the argument
app.add_app("Home", home.app)
app.add_app("COVID-19: Indonesia", indonesia.app)
app.add_app("COVID-19: Jakarta", jakarta.app)
app.add_app("COVID-19: World", world.app)
app.add_app("COVID-19 in Indonesia: Forecast", predictions.app)

# run main app 
app.run()