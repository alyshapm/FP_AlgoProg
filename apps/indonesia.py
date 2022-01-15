import streamlit as st
import plotly.express as px 
import pandas as pd
import plotly.graph_objects as go

def app():
    pd.set_option('display.float_format', lambda x: '%.0f' % x)
    st.title("COVID-19 in Indonesia")
    mapbox_token = "pk.eyJ1IjoiYWx5c2hhcG0iLCJhIjoiY2t4cDg2bTJwMmQ3MjJxcGV3NWJnMXFubiJ9.gyaf72JiPPqj9Aq8-dd0wQ"

    @st.experimental_memo
    def load_data(data):
        return pd.read_csv(data)
    
    # --- FETCH AND CLEAN DATA ---
    df_map = load_data("https://raw.githubusercontent.com/alyshapm/FP_AlgoProg/main/data/kasus_per_provinsi.csv")
    df_jakarta = load_data("https://raw.githubusercontent.com/alyshapm/FP_AlgoProg/main/data/covid_jakarta.csv")
    df_deaths = load_data("https://raw.githubusercontent.com/alyshapm/FP_AlgoProg/main/data/covid_province_death.csv")
    df_confirmed = load_data("https://raw.githubusercontent.com/alyshapm/FP_AlgoProg/main/data/covid_province.csv")
    df_recovered = load_data("https://raw.githubusercontent.com/alyshapm/FP_AlgoProg/main/data/covid_province_recovered.csv")

    date_index = df_deaths.columns[4:]
    total_deaths = df_deaths.melt(
        id_vars=["Province", "Lat", "Long", "Population"], 
        value_vars=date_index,
        var_name="date", 
        value_name="deaths",
    )
    date_index2 = df_confirmed.columns[4:]
    total_confirmed = df_confirmed.melt(
        id_vars=["Province", "Lat", "Long", "Population"], 
        value_vars=date_index2, 
        var_name="date", 
        value_name="confirmed",
    )
    date_index3 = df_recovered.columns[4:]
    total_recovered = df_recovered.melt(
        id_vars=["Province", "Lat", "Long", "Population"], 
        value_vars=date_index3, 
        var_name="date", 
        value_name="recovered",
    )
    df_final = total_confirmed.merge(right=total_deaths, how="left", on=["Province", "Lat", "Long", "Population", "date"])
    df_final = df_final.merge(right=total_recovered, how="left", on=["Province", "Lat", "Long", "Population", "date"])

    df_final["active"] = df_final["confirmed"] - df_final["deaths"] - df_final["recovered"]
    df_final = df_final.groupby(["date", "Province", "Lat", "Long", "Population"])[["confirmed", "deaths", "recovered", "active"]].sum().reset_index()

    df_final["date"] = pd.to_datetime(df_final["date"])
    df_final["date"] = df_final["date"].astype(str) # date needs to be in string format for plotly animations to work
    # df_final = df_final[df_final["Province"] != 0]

    # ---- MAP ---
    st.subheader("Heatmap of COVID-19 in Indonesia")
    info1 = st.expander('About (click to expand)')
    info1.write("This map displays scatter markers using geo-coordinates and can help us identify spatial patterns in our data. The size of markers\
                 is proportional to the number of positive cases in the area.")

    left_row, right_row = st.columns((3, 2))

    fig_map1 = go.Figure(go.Scattermapbox(
        lat=df_map["Lat"],
        lon=df_map["Long"],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size= (df_map["Kasus"] / 70),
            color=df_map["Kasus"],
            colorscale="hsv",
            showscale=False,
            sizemode="area",
            opacity=0.3
        ),
        hoverinfo="text",
        hovertext=
        "Region: " + df_map["Provinsi Asal"].astype(str) + "<br>" +
        "Confirmed: " + [f"{x:,.0f}" for x in df_map["Kasus"]] + "<br>" +
        "Recovered: " + [f"{x:,.0f}" for x in df_map["Sembuh"]] + "<br>" +
        "Deaths: " + [f"{x:,.0f}" for x in df_map["Kematian"]] + "<br>"
    ))
    fig_map1.update_layout(
        autosize=True,
        mapbox_style="dark",
        mapbox=dict(
            accesstoken=mapbox_token,
            center=dict(
                lat=-2.548926,
                lon=118.0148634
            ),
            zoom=3
        ),
        height=600,
        margin=dict(l=0, r=0, b=50, t=0, pad=1)
    )

    fig_map2 = go.Figure(go.Scattermapbox(
        lat=df_jakarta["lat"],
        lon=df_jakarta["long"],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size= (df_jakarta["total_confirmed"]/25),
            color=df_jakarta["total_confirmed"],
            colorscale="hsv",
            showscale=True,
            sizemode="area",
            opacity=0.3
        ),
        hoverinfo="text",
        hovertext=
        "Region: " + df_jakarta["district"].astype(str) + "<br>" ""
        "Confirmed: " + [f"{x:,.0f}" for x in df_jakarta["total_confirmed"]] + "<br>"
    ))
    fig_map2.update_layout(
        autosize=True,
        mapbox_style="dark",
        mapbox=dict(
            accesstoken=mapbox_token,
            center=dict(
                lat=-6.2088,
                lon=106.8456
            ),
            zoom=9,
        ),
        height=600,
        margin=dict(l=0, r=0, b=50, t=0, pad=1)
    )
    
    with left_row:
        st.write("**All of Indonesia**")
        st.plotly_chart(fig_map1, use_container_width=True)
    with right_row:
        st.write("**Jakarta**")
        st.plotly_chart(fig_map2, use_container_width=True)

    # --- GRAPHS PER PROVINCE ---
    list_of_province = df_final["Province"].unique().tolist()

    st.subheader("Line graph by province")
    info2 = st.expander('About (click to expand)')
    info2.write("By selecting more than one province below you can view and compare trends between provinces in Indonesia.")
    
    province_selected = st.multiselect("Select province", list_of_province, default=["Bali", "Jakarta", "Aceh"])
    
    df_final_query = df_final.query("Province in @province_selected")

    @st.experimental_memo
    def plot_per_province(y_axis):
        fig3 = px.line(
            df_final_query, 
            x="date",
            y=y_axis,
            color="Province"
            )
        fig3.update_layout(
            margin=dict(l=0, r=0, b=0, t=0, pad=1)
        )
        return fig3

    row3_1, row3_2 = st.columns((3,3))
    with row3_1:
        st.plotly_chart(plot_per_province("confirmed"), use_container_width=True)
        st.plotly_chart(plot_per_province("recovered"), use_container_width=True)
    with row3_2:
        st.plotly_chart(plot_per_province("deaths"), use_container_width=True)
        st.plotly_chart(plot_per_province("active"), use_container_width=True)
    
    # --- SCATTER ---
    st.subheader("Crossplot timescale")
    info3 = st.expander('About (click to expand)')
    info3.write("A crossplot allows users to plot two features against one another with markers. The marker size here represents \
                the number of COVID-19 death in each country. ")

    @st.experimental_memo
    def scatter_plot(df):
        range_x = [df_final["Population"].min(), df_final["Population"].max() * 1.2]
        range_y = [df_final["confirmed"].min(), df_final["confirmed"].max() * 1.2]
        fig = px.scatter(
            df, x="Population", y = "confirmed", animation_frame=df["date"],
            animation_group="Province", size="deaths", hover_name="Province", color="Province",
            range_x=range_x, range_y=range_y, log_x=True
        )
        fig.update_layout(
            autosize=True,
            height=600,
            margin=dict(l=0, r=0, b=20, t=10, pad=1)
        )
        return fig
    
    # fig4 = px.scatter(
    #     df_final, x="Population", y = "confirmed", animation_frame=df_final["date"],
    #     animation_group="Province", size="deaths", hover_name="Province", color="Province",
    #     range_x=range_x, range_y=range_y, log_x=True
    # )
    # fig4.update_layout(
    #     autosize=True,
    #     height=600,
    #     margin=dict(l=0, r=0, b=20, t=10, pad=1)
    # )

    st.plotly_chart(scatter_plot(df_final), use_container_width=True)