import pandas as pd
from pandas.core.window.rolling import Window
from pandas._config.config import options
from pandas.core.indexing import convert_to_index_sliceable
import streamlit as st
import plotly.graph_objects as go
import plotly_express as px

def app():
    st.title("COVID-19 Worldwide")
    a = st.expander('About (click to expand)')
    a.write("A crossplot allows users to plot two features against one another with markers, marker colour and marker sizes \
    representing third and fourth features.")

    @st.experimental_memo
    def load_data(data):
        return pd.read_csv(data)
    
    df_confirmed = load_data("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    df_deaths = load_data("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    df_recovered = load_data("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    df = load_data("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")

    df_map = df.groupby(["location", "iso_code"])[["total_cases"]].max().reset_index()
    df_map = df_map[~df_map["iso_code"].str.contains('|'.join(["OWID"]))]

    # unpivot data
    date1 = df_confirmed.columns[4:]
    total_confirmed = df_confirmed.melt(
        id_vars=["Province/State", "Country/Region","Lat", "Long"], 
        value_vars=date1, 
        var_name="date", 
        value_name="confirmed"
        )
    date2 = df_deaths.columns[4:]
    total_deaths = df_deaths.melt(
        id_vars=["Province/State", "Country/Region","Lat", "Long"], 
        value_vars=date2, 
        var_name="date", 
        value_name="death"
        )
    date3 = df_recovered.columns[4:]
    total_recovered = df_recovered.melt(
        id_vars=["Province/State", "Country/Region","Lat", "Long"], 
        value_vars=date3, 
        var_name="date", 
        value_name="recovered"
        )

    # merge data frames
    covid_data = total_confirmed.merge(right=total_deaths, how="left", on=["Province/State", "Country/Region","date", "Lat", "Long"])
    covid_data = covid_data.merge(right=total_recovered, how="left", on=["Province/State", "Country/Region","date", "Lat", "Long"])

    # converting data column from str to date format
    covid_data["date"] = pd.to_datetime(covid_data["date"])

    # return missing values NaN
    covid_data.isna().sum()

    # replace NaN with 0
    covid_data["recovered"] = covid_data["recovered"].fillna(0)

    # new column "active"
    covid_data["active"] = covid_data["confirmed"] - covid_data["death"] - covid_data["recovered"]
    covid_data_2 = covid_data.groupby(["date", "Country/Region"])[["confirmed", "death", "recovered", "active"]].sum().reset_index()
    st.write("Last updated: " + str(covid_data_2["date"].iloc[-1].strftime("%B %d, %Y")))

    # --- MAP CHART ---
    scale = [df_map["total_cases"].min(), df_map["total_cases"].max()]

    fig_map = px.choropleth(df_map, locations="iso_code",
                    color="total_cases",
                    hover_name="location", 
                    color_continuous_scale="RdBu",
                    range_color=scale)
    # fig_map.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig_map.update_traces(marker_line_width=0)
    fig_map.update_layout(
        title_text = 'Total confirmed cases in the world',
        autosize=True,
        height=600,
        width=1800,
        margin=dict(l=0, r=0, b=0, t=0, pad=1),
        # geo_bgcolor="rgba(255, 255, 255, 0)",
    )

    st.plotly_chart(fig_map, use_container_width=True)

    country = st.selectbox(
            "Select country:",
            options = list(covid_data["Country/Region"].unique()),
        )

    row1_1, row1_2, row1_3 = st.columns((2,2,2))

    # --- FIRST GRAPH ---
    with row1_1:
        title1 = f"Total cases in {country}"

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=covid_data_2[covid_data_2["Country/Region"] == country]["date"],
                        y=covid_data_2[covid_data_2["Country/Region"] == country]["confirmed"],
                        name="Confirmed",
                        marker_color='red'
                        ))
        fig1.add_trace(go.Bar(x=covid_data_2[covid_data_2["Country/Region"] == country]["date"],
                        y=covid_data_2[covid_data_2["Country/Region"] == country]["recovered"],
                        name='Recovered',
                        marker_color='royalblue'
                        ))
        fig1.add_trace(go.Scatter(x=covid_data_2[covid_data_2["Country/Region"] == country]["date"],
                        y=covid_data_2[covid_data_2["Country/Region"] == country]["death"],
                        name='Deaths',
                        marker_color='gold',    
                    
                        ))
        fig1.update_layout(
        title = title1,
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Covid19 Reported Number of Cases',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.2,
        # margin=dict(l=0, r=0, b=0, t=0, pad=1)
        )

        st.plotly_chart(fig1, use_container_width=True)

    with row1_2:
    # --- SECOND GRAPH ---
        covid_data_3 = covid_data_2[covid_data_2["Country/Region"] == country][["Country/Region", "date", "confirmed"]].reset_index()
        covid_data_3["daily confirmed"] = covid_data_3["confirmed"] - covid_data_3["confirmed"].shift(1)
        covid_data_3["Rolling Avg."] = covid_data_3["daily confirmed"].rolling(window=7).mean()

        title2 = f"Last 30 Days of Confirmed cases in {country}"

        fig2 = px.line(
            x=covid_data_3[covid_data_3["Country/Region"] == country]["date"].tail(30),
            y=covid_data_3[covid_data_3["Country/Region"] == country]["Rolling Avg."].tail(30),
            color=px.Constant("Rolling average"),
            title=title2
        )
        fig2.add_bar(
            x=covid_data_3[covid_data_3["Country/Region"] == country]["date"].tail(30),
            y=covid_data_3[covid_data_3["Country/Region"] == country]["daily confirmed"].tail(30),
            name = "Daily confirmed"
        )
        fig2.update_layout(
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Cumulative cases',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.2,
        # margin=dict(l=0, r=0, b=0, t=0, pad=1)
        )
        st.plotly_chart(fig2, use_container_width=True)
    # --- THIRD GRAPH ---
    with row1_3:
        new_confirmed = covid_data_2[covid_data_2["Country/Region"] == country]["confirmed"].iloc[-1]
        new_deaths = covid_data_2[covid_data_2["Country/Region"] == country]["death"].iloc[-1]
        new_recovered = covid_data_2[covid_data_2["Country/Region"] == country]["recovered"].iloc[-1]
        new_active = covid_data_2[covid_data_2["Country/Region"] == country]["active"].iloc[-1]

        title3 = f"Most recent cases in {country}"
        fig3 = px.pie(
            covid_data_2,
            hole= 0.5,
            names=["Confirmed", "Death", "Recovered", "Active"],
            values=[new_confirmed, new_deaths, new_recovered, new_active],
            title=title3
        )
        fig3.update_layout(
            # margin=dict(l=0, r=0, b=0, t=0, pad=1),
        )
        st.plotly_chart(fig3, use_container_width=True)
