import streamlit as st
import pandas as pd

print("HOTSPOT MODULE LOADED")



def get_hotspot_level(aqi):

    if aqi <= 100:
        return "🟢 Safe Zone"

    elif aqi <= 200:
        return "🟡 Moderate Zone"

    elif aqi <= 300:
        return "🟠 High Risk Zone"

    elif aqi <= 400:
        return "🔴 Severe Hotspot"

    else:
        return "⚫ Critical Hotspot"


def recommendation(aqi):

    if aqi <= 100:
        return "Normal outdoor activities"

    elif aqi <= 200:
        return "Sensitive people should reduce exposure"

    elif aqi <= 300:
        return "Wear mask outdoors"

    elif aqi <= 400:
        return "Avoid prolonged outdoor activities"

    else:
        return "Stay indoors. Health emergency."


def show_hotspot_detection():

    st.title("🔥 AI Hotspot Detection System")

    st.markdown(
        """
        Detect highly polluted locations and identify
        critical AQI hotspots across Ahmedabad.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload AQI Dataset",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info("Upload AQI dataset to begin analysis.")
        return
        
    try:

        df = pd.read_csv(uploaded_file)

        st.success(
            f"{len(df)} records loaded successfully"
        )

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            width="stretch"
        )

    except Exception as e:

        st.error(f"Dataset Error: {e}")
        return

    try:

        locations = pd.read_csv(
            "data/hotspot_locations.csv"
        )
        
        st.success(
            "Location file loaded successfully"
        )

        if len(locations) < len(df):

            locations = locations.sample(
                len(df),
                replace=True,
                random_state=42
            ).reset_index(drop=True)

        else:

            locations = locations.head(
                len(df)
            ).reset_index(drop=True)

        df = pd.concat(
            [
                df.reset_index(drop=True),
                locations
            ],
            axis=1
        )

    except Exception as e:

        st.error(
            f"Location file error: {e}"
        )
        return

    st.subheader("Available Columns")

    st.write(df.columns.tolist())

    if "AQI" not in df.columns:

        st.error(
            "AQI column not found in uploaded dataset."
        )
        return

    location_col = None

    for col in df.columns:

        if col.lower() in [
            "location",
            "area",
            "station",
            "place",
            "location_name"
        ]:

            location_col = col
            break

    if location_col is None:

        df["Location"] = [
            f"Location {i+1}"
            for i in range(len(df))
        ]

        location_col = "Location"

    df["Hotspot_Level"] = df["AQI"].apply(
        get_hotspot_level
    )

    df["Risk_Score"] = round(
        (df["AQI"] / 500) * 100,
        2
    )

    df["Recommendation"] = df["AQI"].apply(
        recommendation
    )

    st.subheader("📊 Hotspot Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Locations",
            len(df)
        )

    with col2:

        st.metric(
            "Critical Hotspots",
            len(df[df["AQI"] > 400])
        )

    with col3:

        st.metric(
            "Severe Hotspots",
            len(
                df[
                    (df["AQI"] > 300)
                    &
                    (df["AQI"] <= 400)
                ]
            )
        )

    with col4:

        st.metric(
            "Average AQI",
            round(df["AQI"].mean(), 2)
        )

    st.markdown("---")

    st.subheader("🔥 Top 10 Hotspots")

    top_hotspots = df.sort_values(
        by="AQI",
        ascending=False
    ).head(10)

    st.dataframe(
        top_hotspots[
            [
                location_col,
                "AQI",
                "Risk_Score",
                "Hotspot_Level"
            ]
        ],
        width="stretch"
    )

    st.markdown("---")

    st.subheader("🚨 Critical Hotspots")

    critical = df[
        df["AQI"] > 300
    ]

    if len(critical) > 0:

        st.dataframe(
            critical[
                [
                    location_col,
                    "AQI",
                    "Risk_Score",
                    "Hotspot_Level",
                    "Recommendation"
                ]
            ],
            width="stretch"
        )

    else:

        st.success(
            "No critical hotspot detected."
        )

    st.markdown("---")

    st.subheader("🤖 AI Recommendations")

    st.dataframe(
        df[
            [
                location_col,
                "AQI",
                "Hotspot_Level",
                "Recommendation"
            ]
        ],
        width="stretch"
    )