import pandas as pd

# ==============================
# Load Dataset
# ==============================

df = pd.read_csv("data/city_hour.csv")

print("Original Shape:", df.shape)

# ==============================
# Select Required Columns
# ==============================

df = df[
    [
        "City",
        "Datetime",
        "PM2.5",
        "PM10",
        "NO2",
        "SO2",
        "CO",
        "O3",
        "AQI"
    ]
]

# ==============================
# Convert Datetime
# ==============================

df["Datetime"] = pd.to_datetime(df["Datetime"])

# ==============================
# Remove Duplicates
# ==============================

df.drop_duplicates(inplace=True)

# ==============================
# Sort by Datetime
# ==============================

df.sort_values("Datetime", inplace=True)

# ==============================
# Remove Rows with Missing AQI
# ==============================

df.dropna(subset=["AQI"], inplace=True)

# ==============================
# Fill Missing Pollutants
# ==============================

pollutants = [
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3"
]

df[pollutants] = df[pollutants].ffill()

# ==============================
# Remove Invalid AQI Values
# CPCB AQI Range = 0 to 500
# ==============================

df = df[(df["AQI"] >= 0) & (df["AQI"] <= 500)]

# ==============================
# Remove Negative Pollutant Values
# ==============================

for col in pollutants:
    df = df[df[col] >= 0]

# ==============================
# Final Information
# ==============================

print("\nFinal Shape:", df.shape)

print("\nAQI Statistics:")
print(df["AQI"].describe())

print("\nMissing Values:")
print(df.isnull().sum())


print("Max AQI:", df["AQI"].max())
print("Min AQI:", df["AQI"].min())

# ==============================
# Save Cleaned Dataset
# ==============================

df.to_csv(
    "data/clean_air_quality.csv",
    index=False
)

print("\nDataset cleaned successfully!")
print("Saved as: data/clean_air_quality.csv")