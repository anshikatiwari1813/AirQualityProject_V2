import streamlit as st
import pandas as pd
import folium

from folium.plugins import HeatMap
from streamlit_folium import st_folium


def get_color(aqi):

    if aqi <= 50:
        return "green"

    elif aqi <= 100:
        return "blue"

    elif aqi <= 200:
        return "orange"

    elif aqi <= 300:
        return "red"

    elif aqi <= 400:
        return "purple"

    else:
        return "black"


def show_gis_map():

    st.title("🌍 GIS AQI Monitoring System")

    st.markdown(
        """
        Interactive GIS Dashboard for
        Air Quality Monitoring and Forecasting
        """
    )

    # =====================================
    # SAMPLE AHMEDABAD STATIONS
    # =====================================

    data = pd.DataFrame({

        "Location": [
            "Bopal",
            "Maninagar",
            "Naroda",
            "Chandkheda",
            "Vastrapur"
        ],

        "Latitude": [
            23.0300,
            22.9950,
            23.0700,
            23.1100,
            23.0400
        ],

        "Longitude": [
            72.4600,
            72.6000,
            72.6700,
            72.5800,
            72.5300
        ],

        "Current_AQI": [
            82,
            135,
            220,
            175,
            95
        ],

        "Forecast_AQI": [
            90,
            145,
            240,
            185,
            100
        ]
    })

    # =====================================
    # MAP
    # =====================================

    m = folium.Map(

        location=[23.0225, 72.5714],

        zoom_start=11,

        tiles="OpenStreetMap"
    )

    # =====================================
    # CURRENT AQI MARKERS
    # =====================================

    for _, row in data.iterrows():

        popup_text = f"""
        <b>{row['Location']}</b><br>

        Current AQI : {row['Current_AQI']}<br>

        Forecast AQI : {row['Forecast_AQI']}
        """

        folium.CircleMarker(

            location=[
                row["Latitude"],
                row["Longitude"]
            ],

            radius=10,

            popup=popup_text,

            color=get_color(
                row["Current_AQI"]
            ),

            fill=True,

            fill_opacity=0.8

        ).add_to(m)

    # =====================================
    # FORECAST LAYER
    # =====================================

    forecast_group = folium.FeatureGroup(
        name="Forecast AQI"
    )

    for _, row in data.iterrows():

        folium.Marker(

            location=[
                row["Latitude"],
                row["Longitude"]
            ],

            popup=f"""
            Forecast AQI:
            {row['Forecast_AQI']}
            """,

            icon=folium.Icon(
                color="cadetblue",
                icon="cloud"
            )

        ).add_to(forecast_group)

    forecast_group.add_to(m)

    # =====================================
    # HEATMAP
    # =====================================

    heat_data = []

    for _, row in data.iterrows():

        heat_data.append([

            row["Latitude"],

            row["Longitude"],

            row["Current_AQI"]

        ])

    HeatMap(

        heat_data,

        radius=25,

        blur=20,

        max_zoom=12

    ).add_to(m)

    # =====================================
    # LEGEND
    # =====================================

    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 220px;
        height: 230px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding:10px;
    ">

    <b>AQI Legend</b><br><br>

    🟢 Good (0-50)<br>

    🔵 Satisfactory (51-100)<br>

    🟠 Moderate (101-200)<br>

    🔴 Poor (201-300)<br>

    🟣 Very Poor (301-400)<br>

    ⚫ Severe (401-500)
    </div>
    """

    m.get_root().html.add_child(
        folium.Element(
            legend_html
        )
    )

    # =====================================
    # LAYER CONTROL
    # =====================================

    folium.LayerControl().add_to(m)

    # =====================================
    # DISPLAY MAP
    # =====================================

    st_folium(

        m,

        width=1200,

        height=650
    )

    # =====================================
    # DATA TABLE
    # =====================================

    st.subheader("📊 AQI Station Information")

    st.dataframe(
        data,
        use_container_width=True
    )

    # =====================================
    # SUMMARY
    # =====================================

    avg_aqi = data["Current_AQI"].mean()

    max_aqi = data["Current_AQI"].max()

    min_aqi = data["Current_AQI"].min()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average AQI",
            round(avg_aqi, 2)
        )

    with col2:
        st.metric(
            "Highest AQI",
            max_aqi
        )

    with col3:
        st.metric(
            "Lowest AQI",
            min_aqi
        )