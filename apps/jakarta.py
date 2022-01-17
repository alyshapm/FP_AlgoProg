from pandas.core.algorithms import mode
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

def app():
    # --- TITLE ---
    st.title("COVID-19 in Jakarta")

    # function to read the csv data
    @st.experimental_memo
    def load_data(data):
        return pd.read_csv(data)

    df_crossplot = load_data("data/covid_jakarta.csv")
    df_extrudingmap = load_data("data/pelanggaran_psbb.csv")
    df_histo = load_data("data/pelanggaran_psbb_timeseries.csv")
    df_airquality = load_data("data/avgcarspeed_jakarta.csv")

    # unpivot data for cross plot 
    cols = list(df_crossplot.columns)
    cols.remove("district")
    cols.remove("region")

    df_melted = pd.melt(df_crossplot, id_vars=["district", "region"], value_vars=cols)

    # --- CROSSPLOT ---
    st.subheader("Crossplot") # title
    info1 = st.expander('About (click to expand)') # info expander
    info1.write("A crossplot allows users to plot two features against one another with markers, marker colour and marker sizes \
    representing third and fourth features.")

    #dictionary for the drop down filters. format is "label" and the corresponding column name
    sizing_labels = {
        "Vaccinated":"vaccinated",
        "Total confirmed":"total_confirmed",
        "Total deaths":"deaths"
    }
    metric_labels = {
        "No. of males":"male",
        "No. of female":"female",
        "Aged 75 or older":"over 75",
        "Population":"population",
        "Life expectancy":"life expectancy"
    }

    row1_1, mid, row2_1 = st.columns((3, 0.5, 3)) # set up container sizes

    # the following are the function for selectbox/drop down menu where users can select the variables for multiple dimensions
    x = row1_1.selectbox("X axis", list(metric_labels.keys())) # drop down box the for x axis
    x_ax = metric_labels[x] # the value of x is then passed through the metric_labels to get the column name

    y = row1_1.selectbox("Y axis", list(metric_labels.keys())) # drop down box the for y axis
    y_ax = metric_labels[y] # the value of y is then passed through the metric_labels to get the column name

    size_by = row2_1.selectbox("Size markers by", list(sizing_labels.keys())) # drop down menu for the markers
    size_by = sizing_labels[size_by] # the value of size_by is then passed through the sizing_labels to get the column name

    color_up = df_melted["district"].drop_duplicates() # drop duplicates so we have one marker for each district

    fig = px.scatter(
        df_melted,
        x=df_melted[df_melted["variable"] == x_ax]["value"], # in the variable column, the data is filtered according to the selected value from the drop down box
        y=df_melted[df_melted["variable"] == y_ax]["value"],
        color=color_up,
        size=df_melted[df_melted["variable"] == size_by]["value"],
        labels=dict(x=x, y=y, color="District")
    )
    fig.update_layout( # update graph layout
        autosize=True,
        height=600,
        margin=dict(l=0, r=0, b=20, t=10, pad=1)
    )

    # plot graph
    st.plotly_chart(fig, use_container_width=True)
    
    # --- EXTRUDING MAP ---
    st.subheader("CRM PSBB Violation Reports in Jakarta") # title
    info2 = st.expander('About (click to expand)') # info box
    info2.write("Distribution of PSBB violation reports from the *Cepat Respon Masyarakat* \
                (Quick Reponse Community) complaint channel in Jakarta.")
    df_histo["date"] = pd.to_datetime(df_histo["date"]) # convert date column to datetime dtype
    st.write("Last updated: " + str(df_histo["date"].iloc[-1].strftime("%B %d, %Y"))) # display last updated by getting the most recent date, as 0 is the first date, -1 will be the last

    # plot graph
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state={
            "latitude": -6.2088, # set view point
            "longitude": 106.8456,
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df_extrudingmap,
                get_position=["long", "lat"], # plot data based to the coordinates
                radius=100,
                elevation_scale=50, # scale of the elevation
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                ),
            ]
        ))

    # --- HISTOGRAM --- 
    fig_histo = px.histogram( 
            df_histo,
            x="date",
            y="total_reports"
        )
    fig_histo.update_traces(
            marker_color="red",
            opacity=0.4
        )
    fig_histo.update_layout( # update graph layout
            autosize=True,
            height=300,
            width=1000,
            margin=dict(l=0, r=0, b=50, t=0, pad=1),
            plot_bgcolor="rgba(0, 0, 0, 0)"
        )
    # plot graph
    st.plotly_chart(fig_histo, use_container_width=True)
    
    # --- BAR-LINE GRAPH ---
    st.subheader("Air Quality vs. Average Transporation Speed during PSBB") # title
    info3 = st.expander('About (click to expand)') # info box
    info3.write("Indeks Standar Pencemaran Udara* (ISPU), or Air Pollution Standard Index in Jakarta\
                during PSBB, from 1 February - 25 November 2020.")

    df_airquality["date"] = pd.to_datetime(df_airquality["date"]) # convert date column to datetime dtype
    st.write("Last updated: " + str(df_airquality["date"].iloc[-1].strftime("%B %d, %Y")))
    
    fig_airquality = px.bar( 
        df_airquality,
        x="date",
        y="ISPU",
        color=df_airquality["Average Speed"],
        color_continuous_scale="RdBu" # there is two data points here, where the length of the bar represents the air quality index and the colour represents the speed
    )
    fig_airquality.update_traces( # disable the border around bar
        marker_line_width = 0,
    )
    fig_airquality.update_layout( # update graph layour
        plot_bgcolor="rgba(0, 0, 0, 0)",
        autosize=True,
        height=400,
        width=1000,
        margin=dict(l=0, r=0, b=50, t=0, pad=1)
    )
    # plot graph
    st.plotly_chart(fig_airquality, use_container_width=True)