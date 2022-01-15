import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title":title, 
            "function":func
            })

    def run(self):
        st.sidebar.title("Navigation")

        app = st.sidebar.selectbox(
            "Select graph",
            self.apps,
            format_func=lambda app: app["title"])

        app['function']()

        st.sidebar.markdown('***')
        st.sidebar.title("About")
        st.sidebar.info(
            "Developed by Alysha Maulidina for Algorithm and Programming final project under Mr. Jude Martinez."
        )

        st.sidebar.markdown('***')
        exp = st.sidebar.expander(label="GitHub & Data Source")
        exp.write('''[<span>Source Code</span>](https://github.com/alyshapm)''', unsafe_allow_html=True)
        exp.write('''[<span>OWID</span>](https://github.com/alyshapm) ''', unsafe_allow_html=True)
        exp.write('''[<span>CSSE at JHU</span>](https://github.com/alyshapm) ''', unsafe_allow_html=True)
        exp.write('''[<span>covid.go.id</span>](https://github.com/alyshapm)''', unsafe_allow_html=True)


        hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)