import pandas as pd

# Load dataset
df = pd.read_csv("data/city_hour.csv")

print("Original Shape:", df.shape)

# Select required columns
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
        "AQI",
        "AQI_Bucket"
    ]
]

# Convert Datetime column
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Sort by datetime
df.sort_values("Datetime", inplace=True)

# Forward fill missing values
df.ffill(inplace=True)

# Remove rows where AQI is still missing
df.dropna(subset=["AQI"], inplace=True)

# Remove unrealistic AQI values
df = df[(df["AQI"] >= 0) & (df["AQI"] <= 500)]

print("Cleaned Shape:", df.shape)

# Check remaining missing values
print("\nRemaining Missing Values:")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv("data/clean_air_quality.csv", index=False)

print("\nDataset cleaned successfully!")
print("File Saved: clean_air_quality.csv")