from enum import auto
import streamlit as st
from PIL import Image

# define class to combine multiple pages
class MultiApp:
    # constructor class that generates a list which stores the pages as an instance variable
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
    # title (in str) is the title of the page which will be added to the list of apps that will be displayed in the dropdown navigation
    # func displays the page in Streamlit
        self.apps.append({
            "title":title, 
            "function":func
            })

    def run(self):
        # --- NAVIGATION ---
        st.sidebar.title("Navigation")
        # dropdown displays list of pages and runs the selected page
        app = st.sidebar.selectbox(
            "Select graph", # label
            self.apps,  # list of options
            format_func=lambda app: app["title"]) # receives the selected page as argument and returns it as str

        # runs the app function
        # app used to access the dictionary and return its corresponding value, or func
        app['function']()

        # --- SIDEBAR STYLING ---
        st.sidebar.markdown('***') # divider

        # info box 1
        st.sidebar.title("About") 
        st.sidebar.info(
            "Developed by Alysha Maulidina for Algorithm and Programming final project under Mr. Jude Martinez."
        )

        # info box 2
        st.sidebar.markdown('***')
        exp = st.sidebar.expander(label="GitHub & Data Source")
        exp.write('''[<span>Source Code</span>](https://github.com/alyshapm/FP_AlgoProg)''', unsafe_allow_html=True)
        exp.write('''[<span>OWID</span>](https://github.com/owid/covid-19-data) ''', unsafe_allow_html=True)
        exp.write('''[<span>HU CSSE COVID-19 Data</span>](hhttps://github.com/CSSEGISandData/COVID-19) ''', unsafe_allow_html=True)
        exp.write('''[<span>covid.go.id</span>](https://covid19.go.id/)''', unsafe_allow_html=True)
        exp.write('''[<span>Corona Jakarta</span>](https://corona.jakarta.go.id/id)''', unsafe_allow_html=True)

        # hides the default Streamlit logo
        hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)