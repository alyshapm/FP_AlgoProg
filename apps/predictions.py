import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px

from prophet.plot import plot_plotly

def app():
    st.title("COVID-19 Forecast in Indonesia")
    a = st.expander('About (click to expand)')
    a.write("A crossplot allows users to plot two features against one another with markers, marker colour and marker sizes \
    representing third and fourth features.")

    df = pd.read_csv("data/covid_indonesia.csv") # read file
    df["Date"] = pd.to_datetime(df["Date"]) # ensure date is in the right format
    df = df.groupby("Date").sum()["total_infected"].reset_index() # groups table by Date and total_infected, removes other columns

    df_prophet = df.rename(columns={"Date":"ds", "total_infected":"y"}) # rename column names for prophet complience

    fig1 = px.area(
        df,
        x= df["Date"],
        y= df["total_infected"],
    )
    st.plotly_chart(fig1, use_container_width=True)


    m = Prophet(
        changepoint_prior_scale=0.3,
        changepoint_range=0.99,
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=True,
        seasonality_mode='additive'
        )
    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=30) # build future dataframe for 30 days
    forecast = m.predict(future)
    
    fig2 = plot_plotly(m, forecast)
    st.plotly_chart(fig2, use_container_width=True)