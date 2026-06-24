import pandas as pd

# ==============================
# Load Clean Dataset
# ==============================

df = pd.read_csv("data/clean_air_quality.csv")

# Safety Filter
df = df[(df["AQI"] >= 0) & (df["AQI"] <= 500)]

# ==============================
# PM2.5 Sub Index
# ==============================

def pm25_subindex(x):

    if x <= 30:
        return (50 / 30) * x

    elif x <= 60:
        return 51 + ((100 - 51) / (60 - 31)) * (x - 31)

    elif x <= 90:
        return 101 + ((200 - 101) / (90 - 61)) * (x - 61)

    elif x <= 120:
        return 201 + ((300 - 201) / (120 - 91)) * (x - 91)

    elif x <= 250:
        return 301 + ((400 - 301) / (250 - 121)) * (x - 121)

    else:
        return 500


# ==============================
# PM10 Sub Index
# ==============================

def pm10_subindex(x):

    if x <= 50:
        return x

    elif x <= 100:
        return 51 + ((100 - 51) / (100 - 51)) * (x - 51)

    elif x <= 250:
        return 101 + ((200 - 101) / (250 - 101)) * (x - 101)

    elif x <= 350:
        return 201 + ((300 - 201) / (350 - 251)) * (x - 251)

    elif x <= 430:
        return 301 + ((400 - 301) / (430 - 351)) * (x - 351)

    else:
        return 500


# ==============================
# NO2 Sub Index
# ==============================

def no2_subindex(x):

    if x <= 40:
        return (50 / 40) * x

    elif x <= 80:
        return 51 + ((100 - 51) / (80 - 41)) * (x - 41)

    elif x <= 180:
        return 101 + ((200 - 101) / (180 - 81)) * (x - 81)

    elif x <= 280:
        return 201 + ((300 - 201) / (280 - 181)) * (x - 181)

    elif x <= 400:
        return 301 + ((400 - 301) / (400 - 281)) * (x - 281)

    else:
        return 500


# ==============================
# SO2 Sub Index
# ==============================

def so2_subindex(x):

    if x <= 40:
        return (50 / 40) * x

    elif x <= 80:
        return 51 + ((100 - 51) / (80 - 41)) * (x - 41)

    elif x <= 380:
        return 101 + ((200 - 101) / (380 - 81)) * (x - 81)

    elif x <= 800:
        return 201 + ((300 - 201) / (800 - 381)) * (x - 381)

    elif x <= 1600:
        return 301 + ((400 - 301) / (1600 - 801)) * (x - 801)

    else:
        return 500


# ==============================
# CO Sub Index
# ==============================

def co_subindex(x):

    if x <= 1:
        return 50 * x

    elif x <= 2:
        return 51 + ((100 - 51) / (2 - 1)) * (x - 1)

    elif x <= 10:
        return 101 + ((200 - 101) / (10 - 2)) * (x - 2)

    elif x <= 17:
        return 201 + ((300 - 201) / (17 - 10)) * (x - 10)

    elif x <= 34:
        return 301 + ((400 - 301) / (34 - 17)) * (x - 17)

    else:
        return 500


# ==============================
# O3 Sub Index
# ==============================

def o3_subindex(x):

    if x <= 50:
        return x

    elif x <= 100:
        return 51 + ((100 - 51) / (100 - 51)) * (x - 51)

    elif x <= 168:
        return 101 + ((200 - 101) / (168 - 101)) * (x - 101)

    elif x <= 208:
        return 201 + ((300 - 201) / (208 - 169)) * (x - 169)

    elif x <= 748:
        return 301 + ((400 - 301) / (748 - 209)) * (x - 209)

    else:
        return 500


# ==============================
# Calculate Sub Indices
# ==============================

df["PM25_SubIndex"] = df["PM2.5"].apply(pm25_subindex)
df["PM10_SubIndex"] = df["PM10"].apply(pm10_subindex)
df["NO2_SubIndex"] = df["NO2"].apply(no2_subindex)
df["SO2_SubIndex"] = df["SO2"].apply(so2_subindex)
df["CO_SubIndex"] = df["CO"].apply(co_subindex)
df["O3_SubIndex"] = df["O3"].apply(o3_subindex)

# ==============================
# Clip all SubIndices
# ==============================

sub_cols = [
    "PM25_SubIndex",
    "PM10_SubIndex",
    "NO2_SubIndex",
    "SO2_SubIndex",
    "CO_SubIndex",
    "O3_SubIndex"
]

for col in sub_cols:
    df[col] = df[col].clip(0, 500)

# ==============================
# Final AQI
# ==============================

df["Calculated_AQI"] = df[sub_cols].max(axis=1)

df["Calculated_AQI"] = df["Calculated_AQI"].clip(0, 500)

# ==============================
# AQI Category
# ==============================

def classify_aqi(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


df["Calculated_Category"] = df["Calculated_AQI"].apply(classify_aqi)

# ==============================
# Error Analysis
# ==============================

df["AQI_Error"] = abs(df["AQI"] - df["Calculated_AQI"])

print("\nAverage Error:")
print(df["AQI_Error"].mean())

print("\nMedian Error:")
print(df["AQI_Error"].median())

print("\nSample Results:\n")

print(
    df[
        [
            "AQI",
            "Calculated_AQI",
            "Calculated_Category"
        ]
    ].head()
)

# ==============================
# Save Results
# ==============================

df.to_csv(
    "data/final_aqi_output.csv",
    index=False
)

print("\nAQI Calculation Engine Completed Successfully!")
print("File Saved: data/final_aqi_output.csv")