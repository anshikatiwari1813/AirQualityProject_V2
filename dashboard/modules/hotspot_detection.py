import streamlit as st
import pandas as pd

print("HOTSPOT MODULE LOADED")


def get_hotspot_level(aqi):

    try:

        aqi = float(aqi)

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

    except:

        return "Unknown"


def recommendation(aqi):

    try:

        aqi = float(aqi)

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

    except:

        return "No recommendation available"


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

        st.info(
            "Upload AQI dataset to begin analysis."
        )

        return

    # =====================================
    # LOAD DATASET
    # =====================================

    try:

        df = pd.read_csv(uploaded_file)

        # REMOVE DUPLICATE COLUMNS
        df = df.loc[:, ~df.columns.duplicated()]

        st.success(
            f"{len(df)} records loaded successfully"
        )

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Dataset Error: {e}"
        )

        return

    # =====================================
    # LOAD LOCATION FILE
    # =====================================

    try:

        locations = pd.read_csv(
            "data/hotspot_locations.csv"
        )

        locations = locations.loc[
            :,
            ~locations.columns.duplicated()
        ]

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

        if "Location" in df.columns:

            df.drop(
                columns=["Location"],
                inplace=True
            )

        df = pd.concat(
            [
                df.reset_index(drop=True),
                locations
            ],
            axis=1
        )

        # REMOVE DUPLICATE COLUMNS AGAIN
        df = df.loc[:, ~df.columns.duplicated()]

    except Exception as e:

        st.error(
            f"Location file error: {e}"
        )

        return

    # =====================================
    # DETECT AQI COLUMN
    # =====================================

    if "AQI" in df.columns:

        aqi_col = "AQI"

    elif "Calculated_AQI" in df.columns:

        aqi_col = "Calculated_AQI"

    elif "predicted_aqi" in df.columns:

        aqi_col = "predicted_aqi"

    else:

        st.error(
            "AQI column not found."
        )

        st.write(
            "Available Columns:"
        )

        st.write(
            df.columns.tolist()
        )

        return

    # =====================================
    # FIX DUPLICATE AQI COLUMN ISSUE
    # =====================================

    if isinstance(
        df[aqi_col],
        pd.DataFrame
    ):

        df[aqi_col] = df[
            aqi_col
        ].iloc[:, 0]

    df[aqi_col] = pd.to_numeric(
        df[aqi_col],
        errors="coerce"
    )

    df = df.dropna(
        subset=[aqi_col]
    )

    # =====================================
    # LOCATION COLUMN
    # =====================================

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

    # =====================================
    # HOTSPOT ANALYSIS
    # =====================================

    df["Hotspot_Level"] = df[
        aqi_col
    ].apply(
        get_hotspot_level
    )

    df["Risk_Score"] = round(
        (df[aqi_col] / 500) * 100,
        2
    )

    df["Recommendation"] = df[
        aqi_col
    ].apply(
        recommendation
    )

    # =====================================
    # SUMMARY
    # =====================================

    st.subheader(
        "📊 Hotspot Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Locations",
            len(df)
        )

    with col2:

        st.metric(
            "Critical Hotspots",
            len(
                df[
                    df[aqi_col] > 400
                ]
            )
        )

    with col3:

        st.metric(
            "Severe Hotspots",
            len(
                df[
                    (df[aqi_col] > 300)
                    &
                    (df[aqi_col] <= 400)
                ]
            )
        )

    with col4:

        st.metric(
            "Average AQI",
            round(
                df[aqi_col].mean(),
                2
            )
        )

    st.markdown("---")

    # =====================================
    # TOP 10 HOTSPOTS
    # =====================================

    st.subheader(
        "🔥 Top 10 Hotspots"
    )

    top_hotspots = df.sort_values(
        by=aqi_col,
        ascending=False
    ).head(10)

    st.dataframe(
        top_hotspots[
            [
                location_col,
                aqi_col,
                "Risk_Score",
                "Hotspot_Level"
            ]
        ],
        use_container_width=True
    )

    st.markdown("---")

    # =====================================
    # CRITICAL HOTSPOTS
    # =====================================

    st.subheader(
        "🚨 Critical Hotspots"
    )

    critical = df[
        df[aqi_col] > 300
    ]

    if len(critical) > 0:

        st.dataframe(
            critical[
                [
                    location_col,
                    aqi_col,
                    "Risk_Score",
                    "Hotspot_Level",
                    "Recommendation"
                ]
            ],
            use_container_width=True
        )

    else:

        st.success(
            "No critical hotspot detected."
        )

    st.markdown("---")

    # =====================================
    # AI RECOMMENDATIONS
    # =====================================

    st.subheader(
        "🤖 AI Recommendations"
    )

    st.dataframe(
        df[
            [
                location_col,
                aqi_col,
                "Hotspot_Level",
                "Recommendation"
            ]
        ],
        use_container_width=True
    )

    # =====================================
    # DOWNLOAD REPORT
    # =====================================

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "⬇ Download Hotspot Report",
        csv,
        "hotspot_report.csv",
        "text/csv"
    )