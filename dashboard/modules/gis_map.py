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


def get_category(aqi):

    if aqi <= 50:
        return "Good 🟢"

    elif aqi <= 100:
        return "Satisfactory 🔵"

    elif aqi <= 200:
        return "Moderate 🟠"

    elif aqi <= 300:
        return "Poor 🔴"

    elif aqi <= 400:
        return "Very Poor 🟣"

    else:
        return "Severe ⚫"


def show_gis_map():

    st.title("🌍 GIS AQI Monitoring Dashboard")

    st.markdown("""
    Interactive GIS-based Air Quality Monitoring
    and Forecasting Dashboard
    """)

    try:

        data = pd.read_csv(
            "data/hotspot_locations.csv"
        )

    except Exception as e:

        st.error(
            f"Error loading hotspot_locations.csv: {e}"
        )

        return

    if data.empty:

        st.warning(
            "No hotspot data available."
        )

        return

    # =========================
    # AQI CATEGORY
    # =========================

    data["Category"] = data["AQI"].apply(
        get_category
    )

    # =========================
    # DASHBOARD FILTERS
    # =========================

    st.subheader("🎛 GIS Filters")

    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:

        category_filter = st.selectbox(

            "AQI Category",

            ["All"] +
            sorted(
                data["Category"].unique()
            )

        )

    with col_filter2:

        selected_location = st.selectbox(

            "Focus Location",

            data["Location"]

        )

    if category_filter != "All":

        data = data[
            data["Category"]
            == category_filter
        ]

    selected_row = data[
        data["Location"]
        == selected_location
    ].iloc[0]

    # =========================
    # CREATE MAP
    # =========================

    m = folium.Map(

        location=[
            selected_row["Latitude"],
            selected_row["Longitude"]
        ],

        zoom_start=11,

        tiles="OpenStreetMap"

    )

    # =========================
    # CURRENT AQI LAYER
    # =========================

    current_layer = folium.FeatureGroup(
        name="Current AQI"
    )

    for _, row in data.iterrows():

        marker_color = get_color(
            row["AQI"]
        )

        popup_text = f"""
        <b>{row['Location']}</b><br>

        Current AQI : {row['AQI']}<br>

        Forecast AQI : {row['Forecast_AQI']}<br>

        Category : {row['Category']}
        """

        folium.CircleMarker(

            location=[
                row["Latitude"],
                row["Longitude"]
            ],

            radius=12,

            popup=popup_text,

            color=marker_color,

            fill=True,

            fill_color=marker_color,

            fill_opacity=0.9,

            weight=3

        ).add_to(
            current_layer
        )

    current_layer.add_to(m)

    # =========================
    # FORECAST AQI LAYER
    # =========================

    forecast_layer = folium.FeatureGroup(
        name="Forecast AQI"
    )

    for _, row in data.iterrows():

        folium.Marker(

            location=[
                row["Latitude"],
                row["Longitude"]
            ],

            popup=f"""
            <b>{row['Location']}</b><br>

            Forecast AQI :
            {row['Forecast_AQI']}
            """,

            icon=folium.Icon(
                color="cadetblue",
                icon="cloud"
            )

        ).add_to(
            forecast_layer
        )

    forecast_layer.add_to(m)

    # =========================
    # HEATMAP
    # =========================

    heat_data = []

    for _, row in data.iterrows():

        heat_data.append([

            row["Latitude"],

            row["Longitude"],

            row["AQI"]

        ])

    HeatMap(

        heat_data,

        radius=25,

        blur=20,

        max_zoom=12

    ).add_to(m)

    # =========================
    # AQI LEGEND
    # =========================

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

    # =========================
    # LAYER CONTROL
    # =========================

    folium.LayerControl().add_to(m)

    # =========================
    # DISPLAY MAP
    # =========================

    st_folium(

        m,

        width=1200,

        height=650

    )

    # =========================
    # AQI STATION TABLE
    # =========================

    st.subheader(
        "📊 AQI Hotspot Information"
    )

    st.dataframe(

        data,

        use_container_width=True

    )

    # =========================
    # SUMMARY METRICS
    # =========================

    avg_aqi = data["AQI"].mean()

    max_aqi = data["AQI"].max()

    min_aqi = data["AQI"].min()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average AQI",
            round(avg_aqi, 2)
        )

    with col2:

        st.metric(
            "Highest AQI",
            int(max_aqi)
        )

    with col3:

        st.metric(
            "Lowest AQI",
            int(min_aqi)
        )

    st.success(
        "GIS AQI Dashboard Loaded Successfully"
    )