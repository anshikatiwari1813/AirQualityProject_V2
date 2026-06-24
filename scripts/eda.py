import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Load dataset
df = pd.read_csv("data/clean_air_quality.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

# ------------------------------------
# Convert Datetime
# ------------------------------------
df["Datetime"] = pd.to_datetime(df["Datetime"])

# ------------------------------------
# AQI Distribution
# ------------------------------------
plt.figure(figsize=(8,5))
plt.hist(df["AQI"], bins=50)
plt.title("AQI Distribution")
plt.xlabel("AQI")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("outputs/aqi_distribution.png")
plt.close()

print("AQI Distribution Saved")

# ------------------------------------
# Pollutant Distributions
# ------------------------------------
pollutants = ["PM2.5","PM10","NO2","SO2","CO","O3"]

for col in pollutants:
    plt.figure(figsize=(8,5))
    plt.hist(df[col], bins=50)
    plt.title(f"{col} Distribution")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"outputs/{col}_distribution.png")
    plt.close()

print("Pollutant Distributions Saved")

# ------------------------------------
# Correlation Heatmap
# ------------------------------------
plt.figure(figsize=(10,8))

sns.heatmap(
    df[["PM2.5","PM10","NO2","SO2","CO","O3","AQI"]]
    .corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png")
plt.close()

print("Correlation Heatmap Saved")

# ------------------------------------
# AQI Categories
# ------------------------------------
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

df["AQI_Category"] = df["AQI"].apply(classify_aqi)

plt.figure(figsize=(8,5))

df["AQI_Category"].value_counts().plot(
    kind="bar"
)

plt.title("AQI Category Distribution")
plt.xlabel("Category")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/category_distribution.png")
plt.close()

print("AQI Category Distribution Saved")

# ------------------------------------
# Monthly AQI Trend
# ------------------------------------
df["Month"] = df["Datetime"].dt.month

monthly_aqi = df.groupby("Month")["AQI"].mean()

plt.figure(figsize=(10,5))
monthly_aqi.plot(marker="o")

plt.title("Monthly Average AQI")
plt.xlabel("Month")
plt.ylabel("Average AQI")
plt.grid(True)

plt.tight_layout()
plt.savefig("outputs/monthly_aqi_trend.png")
plt.close()

print("Monthly AQI Trend Saved")

# ------------------------------------
# Top Polluted Cities
# ------------------------------------
top_cities = (
    df.groupby("City")["AQI"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,5))

top_cities.plot(kind="bar")

plt.title("Top 10 Most Polluted Cities")
plt.xlabel("City")
plt.ylabel("Average AQI")

plt.tight_layout()
plt.savefig("outputs/top_polluted_cities.png")
plt.close()

print("Top Polluted Cities Chart Saved")

# ------------------------------------
# Summary Statistics
# ------------------------------------
print("\nAQI Statistics:")
print(df["AQI"].describe())

print("\nCorrelation with AQI:")
print(
    df[
        ["PM2.5","PM10","NO2","SO2","CO","O3","AQI"]
    ]
    .corr()["AQI"]
    .sort_values(ascending=False)
)

print("\nEDA Completed Successfully!")
print("Charts saved in outputs folder.")