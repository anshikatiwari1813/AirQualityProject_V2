import streamlit as st

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Air Quality Prediction & Monitoring System",
    page_icon="🌍",
    layout="wide"
)

# ====================================
# IMPORT MODULES
# ====================================

from modules.home import show_home
from modules.upload import show_upload
from modules.eda import show_eda
from modules.aqi_calculator import show_aqi_calculator
from modules.xgboost_prediction import show_xgboost_prediction
import modules.forecasting as forecasting
from modules.explainability import show_explainability
from modules.gis_map import show_gis_map
from modules.source_attribution import show_source_attribution
from modules.hotspot_detection import show_hotspot_detection
from modules.alert_center import show_alert_center
from modules.health import show_health
from modules.prediction_history import show_prediction_history
from modules.database_analytics import show_database_analytics
from modules.reports import show_reports
from modules.about import show_about

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("🌍 Air Quality System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Dataset Upload",
        "EDA Dashboard",
        "AQI Calculator",
        "AQI Prediction (XGBoost)",
        "LSTM Forecasting",
        "Explainable AI",
        "GIS AQI Map",
        "Source Attribution",
        "Hotspot Detection",
        "Alert Center",
        "Health Advisory",
        "Prediction History",
        "Database Analytics",
        "Reports",
        "About"
    ]
)

# ====================================
# PAGE ROUTING
# ====================================

if page == "Home":
    show_home()

elif page == "Dataset Upload":
    show_upload()

elif page == "EDA Dashboard":
    show_eda()

elif page == "AQI Calculator":
    show_aqi_calculator()

elif page == "AQI Prediction (XGBoost)":
    show_xgboost_prediction()
elif page == "LSTM Forecasting":
    forecasting.show_forecasting()

elif page == "Explainable AI":
    show_explainability()

elif page == "GIS AQI Map":
    show_gis_map()

elif page == "Source Attribution":
    show_source_attribution()

elif page == "Hotspot Detection":
    show_hotspot_detection()

elif page == "Alert Center":
    show_alert_center()

elif page == "Health Advisory":
    show_health()

elif page == "Prediction History":
    show_prediction_history()

elif page == "Database Analytics":
    show_database_analytics()

elif page == "Reports":
    show_reports()

elif page == "About":
    show_about()
