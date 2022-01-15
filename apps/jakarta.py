from pandas.core.algorithms import mode
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

def app():
    st.title("COVID-19 in Jakarta")

    df_crossplot = pd.read_csv("covid_jakarta.csv")
    df_extrudingmap = pd.read_csv("pelanggaran_psbb.csv")
    df_histo = pd.read_csv("pelanggaran_psbb_timeseries.csv")
    df_airquality = pd.read_csv("avgcarspeed_jakarta.csv")

    cols = list(df_crossplot.columns)
    cols.remove("district")
    cols.remove("region")

    df_melted = pd.melt(df_crossplot, id_vars=["district", "region"], value_vars=cols)

    # --- CROSSPLOT ---
    st.subheader("Crossplot")
    info1 = st.expander('About (click to expand)')
    info1.write("A crossplot allows users to plot two features against one another with markers, marker colour and marker sizes \
    representing third and fourth features.")

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

    row1_1, mid, row2_1 = st.columns((3, 0.5, 3))

    x = row1_1.selectbox("X axis", list(metric_labels.keys()))
    x_ax = metric_labels[x]

    y = row1_1.selectbox("Y axis", list(metric_labels.keys()))
    y_ax = metric_labels[y]

    size_by = row2_1.selectbox("Size markers by", list(sizing_labels.keys()))
    size_by = sizing_labels[size_by]

    # region_list = list(df_melted["region"].unique())
    # region_list.sort()
    # region_list.insert(0, "Show all districts")

    # region = st.selectbox("Show which region", region_list)

    # if region != "Show all districs":
    #     df_melted = df_melted[df_melted["region"] == region]

    color_up = df_melted["district"].drop_duplicates()

    fig = px.scatter(
        df_melted,
        x=df_melted[df_melted["variable"] == x_ax]["value"],
        y=df_melted[df_melted["variable"] == y_ax]["value"],
        color=color_up,
        size=df_melted[df_melted["variable"] == size_by]["value"],
        labels=dict(x=x, y=y, color="District")
    )
    fig.update_layout(
        autosize=True,
        height=600,
        margin=dict(l=0, r=0, b=20, t=10, pad=1)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # --- EXTRUDING MAP ---
    st.subheader("CRM PSBB Violation Reports in Jakarta")
    info2 = st.expander('About (click to expand)')
    info2.write("Distribution of PSBB violation reports from the *Cepat Respon Masyarakat* \
                (Quick Reponse Community) complaint channel in Jakarta.")

    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state={
            "latitude": -6.2088,
            "longitude": 106.8456,
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df_extrudingmap,
                get_position=["long", "lat"],
                radius=100,
                elevation_scale=50,
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
    fig_histo.update_layout(
        autosize=True,
        height=300,
        width=1000,
        margin=dict(l=0, r=0, b=50, t=0, pad=1),
        plot_bgcolor="rgba(0, 0, 0, 0)"
    )

    st.plotly_chart(fig_histo, use_container_width=True)
    
    # --- BAR-LINE GRAPH ---
    st.subheader("Air Quality vs. Average Transporation Speed during PSBB")
    info3 = st.expander('About (click to expand)')
    info3.write("Indeks Standar Pencemaran Udara* (ISPU), or Air Pollution Standard Index in Jakarta\
                during PSBB, from 1 February - 25 November 2020.")
    
    fig_airquality = px.bar(
        df_airquality,
        x="date",
        y="ISPU",
        color=df_airquality["Average Speed"],
        color_continuous_scale="RdBu"
    )
    fig_airquality.update_traces(
        marker_line_color = 'rgb(0, 2, 1)'
    )
    fig_airquality.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        autosize=True,
        height=400,
        width=1000,
        margin=dict(l=0, r=0, b=50, t=0, pad=1)
    )

    st.plotly_chart(fig_airquality, use_container_width=True)