import pandas as pd
import os

# Create output folder if needed
os.makedirs("data", exist_ok=True)

# Load cleaned dataset
df = pd.read_csv("data/clean_air_quality.csv")

print("Original Shape:")
print(df.shape)

# ----------------------------------
# Convert Datetime
# ----------------------------------
df["Datetime"] = pd.to_datetime(df["Datetime"])

# ----------------------------------
# Time Features
# ----------------------------------
df["Hour"] = df["Datetime"].dt.hour
df["Day"] = df["Datetime"].dt.day
df["Month"] = df["Datetime"].dt.month
df["Year"] = df["Datetime"].dt.year
df["Weekday"] = df["Datetime"].dt.weekday

print("Time Features Created")

# ----------------------------------
# Season Feature
# ----------------------------------
def get_season(month):

    if month in [12, 1, 2]:
        return 1   # Winter

    elif month in [3, 4, 5]:
        return 2   # Summer

    elif month in [6, 7, 8, 9]:
        return 3   # Monsoon

    else:
        return 4   # Post Monsoon

df["Season"] = df["Month"].apply(get_season)

print("Season Feature Created")

# ----------------------------------
# Sort Data
# ----------------------------------
df = df.sort_values(
    by=["City", "Datetime"]
)

# ----------------------------------
# Lag Features
# ----------------------------------
df["AQI_Lag_1"] = df.groupby("City")["AQI"].shift(1)
df["AQI_Lag_6"] = df.groupby("City")["AQI"].shift(6)
df["AQI_Lag_24"] = df.groupby("City")["AQI"].shift(24)

print("Lag Features Created")

# ----------------------------------
# Rolling Average Features
# ----------------------------------
df["AQI_Rolling_6"] = (
    df.groupby("City")["AQI"]
      .transform(lambda x: x.rolling(6).mean())
)

df["AQI_Rolling_24"] = (
    df.groupby("City")["AQI"]
      .transform(lambda x: x.rolling(24).mean())
)

print("Rolling Features Created")

# ----------------------------------
# Remove rows with NaN generated
# from lag and rolling features
# ----------------------------------
df.dropna(inplace=True)

print("\nFinal Shape:")
print(df.shape)

# ----------------------------------
# Save Feature Dataset
# ----------------------------------
output_file = "data/feature_dataset.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nFeature Engineering Completed Successfully!")
print(f"Saved as: {output_file}")

# ----------------------------------
# Show Sample
# ----------------------------------
print("\nSample Data:")
print(
    df[
        [
            "City",
            "Datetime",
            "AQI",
            "Hour",
            "Month",
            "Season",
            "AQI_Lag_1",
            "AQI_Lag_6",
            "AQI_Lag_24",
            "AQI_Rolling_6",
            "AQI_Rolling_24"
        ]
    ].head()
)