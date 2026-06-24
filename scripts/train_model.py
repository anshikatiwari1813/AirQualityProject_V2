import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# -----------------------------------
# Load Dataset
# -----------------------------------
df = pd.read_csv("data/feature_dataset.csv")

print("Dataset Shape:")
print(df.shape)

# -----------------------------------
# Features
# -----------------------------------
features = [
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3",
    "Hour",
    "Day",
    "Month",
    "Year",
    "Weekday",
    "Season",
    "AQI_Lag_1",
    "AQI_Lag_6",
    "AQI_Lag_24",
    "AQI_Rolling_6",
    "AQI_Rolling_24"
]

target = "AQI"

X = df[features]
y = df[target]

# -----------------------------------
# Train Test Split
# -----------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ===================================
# RANDOM FOREST
# ===================================
print("\n" + "="*50)
print("TRAINING RANDOM FOREST")
print("="*50)

rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_pred)
rf_rmse = mean_squared_error(y_test, rf_pred) ** 0.5
rf_r2 = r2_score(y_test, rf_pred)

print("\nRandom Forest Results")
print("MAE :", round(rf_mae, 2))
print("RMSE:", round(rf_rmse, 2))
print("R2  :", round(rf_r2, 4))

# ===================================
# XGBOOST
# ===================================
print("\n" + "="*50)
print("TRAINING XGBOOST")
print("="*50)

xgb_model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb_model.fit(X_train, y_train)

xgb_pred = xgb_model.predict(X_test)

xgb_mae = mean_absolute_error(y_test, xgb_pred)
xgb_rmse = mean_squared_error(y_test, xgb_pred) ** 0.5
xgb_r2 = r2_score(y_test, xgb_pred)

print("\nXGBoost Results")
print("MAE :", round(xgb_mae, 2))
print("RMSE:", round(xgb_rmse, 2))
print("R2  :", round(xgb_r2, 4))

# ===================================
# SAVE BEST MODEL
# ===================================
if xgb_r2 > rf_r2:

    best_model = xgb_model
    best_name = "XGBoost"

    joblib.dump(
        xgb_model,
        "models/best_aqi_model.pkl"
    )

else:

    best_model = rf_model
    best_name = "RandomForest"

    joblib.dump(
        rf_model,
        "models/best_aqi_model.pkl"
    )

print("\n" + "="*50)
print("BEST MODEL:", best_name)
print("="*50)

# ===================================
# FEATURE IMPORTANCE
# ===================================
if best_name == "XGBoost":

    importance = pd.DataFrame({
        "Feature": features,
        "Importance": xgb_model.feature_importances_
    })

else:

    importance = pd.DataFrame({
        "Feature": features,
        "Importance": rf_model.feature_importances_
    })

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Important Features:\n")
print(importance.head(10))

# Save importance report
importance.to_csv(
    "feature_importance.csv",
    index=False
)

print("\nModel Saved:")
print("models/best_aqi_model.pkl")

print("\nFeature Importance Saved:")
print("feature_importance.csv")

print("\nTraining Completed Successfully!")