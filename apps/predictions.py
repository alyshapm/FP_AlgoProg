import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px

from prophet.plot import plot_plotly

def app():
    st.title("COVID-19 Forecast in Indonesia")
    a = st.expander('About (click to expand)')
    a.write("The second graph shows a 3-month ahead forecast of confirmed cases of COVID-19 in Indonesia using Prophet.\
            Hover over the tail of the graph to see predicted number.")

    df = pd.read_csv("data/covid_indonesia.csv") # read file
    df["Date"] = pd.to_datetime(df["Date"]) # ensure date is in the right format
    df = df.groupby("Date").sum()["total_infected"].reset_index() # groups table by Date and total_infected, removes other columns

    df_prophet = df.rename(columns={"Date":"ds", "total_infected":"y"}) # rename column names so that prophet can read them

    st.subheader("Total Cumulative Infections in Indonesia") # plot graph of confirmed cases so that we can compare agaisnt projected values
    fig1 = px.area(
        df,
        x= df["Date"],
        y= df["total_infected"],
    )
    fig1.update_layout(
                   xaxis_title='date',
                   yaxis_title='Infected'
                    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("COVID-19 Projections in 3 months") # build forecast model
    m = Prophet(
        # time series frquently have abrupt changes in their trajectories, and prophet will detect these "changepoints" so to adapt it appropriately. 
        # the changepoint_prior_scale value will increases trend flexibility
        changepoint_prior_scale=0.3, 
        changepoint_range=0.99, # prophet will place potential change points in the first 99% of the time series
        daily_seasonality=True,
        seasonality_mode='additive'
        )
    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=30*3) # daily predictions for 3 months
    forecast = m.predict(future)
    
    fig2 = plot_plotly(m, forecast) # plot prediction graph
    st.plotly_chart(fig2, use_container_width=True)