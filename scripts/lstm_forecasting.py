import pandas as pd
import numpy as np
import os
import joblib

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Dropout
)

from tensorflow.keras.callbacks import EarlyStopping

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv(
    "data/feature_dataset.csv"
)

print("Dataset Shape:")
print(df.shape)

# =====================================
# FEATURES
# =====================================

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
    "Season",
    "AQI_Lag_1",
    "AQI_Lag_6",
    "AQI_Lag_24",
    "AQI_Rolling_6",
    "AQI_Rolling_24"
]

target = "AQI"

# =====================================
# CLEAN DATA
# =====================================

df = df.dropna()

print("\nShape After Cleaning:")
print(df.shape)

# =====================================
# SCALE FEATURES
# =====================================

feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

X_scaled = feature_scaler.fit_transform(
    df[features]
)

y_scaled = target_scaler.fit_transform(
    df[[target]]
)

# =====================================
# SAVE SCALERS
# =====================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    feature_scaler,
    "models/feature_scaler.pkl"
)

joblib.dump(
    target_scaler,
    "models/target_scaler.pkl"
)

print("\nScalers Saved Successfully")

# =====================================
# CREATE SEQUENCES
# =====================================

sequence_length = 24

X = []
y = []

for i in range(
    sequence_length,
    len(df)
):

    X.append(
        X_scaled[
            i-sequence_length:i
        ]
    )

    y.append(
        y_scaled[i]
    )

X = np.array(X)
y = np.array(y)

print("\nSequence Shape:")
print(X.shape)

# =====================================
# TRAIN TEST SPLIT
# =====================================

split = int(
    len(X) * 0.8
)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]

print(
    "\nTraining Samples:",
    len(X_train)
)

print(
    "Testing Samples:",
    len(X_test)
)

# =====================================
# BUILD LSTM MODEL
# =====================================

model = Sequential()

model.add(
    LSTM(
        128,
        return_sequences=True,
        input_shape=(
            X_train.shape[1],
            X_train.shape[2]
        )
    )
)

model.add(
    Dropout(0.2)
)

model.add(
    LSTM(64)
)

model.add(
    Dropout(0.2)
)

model.add(
    Dense(
        32,
        activation="relu"
    )
)

model.add(
    Dense(1)
)

# =====================================
# COMPILE MODEL
# =====================================

model.compile(
    optimizer="adam",
    loss="mse"
)

print("\nModel Summary:")
model.summary()

# =====================================
# EARLY STOPPING
# =====================================

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=2,
    restore_best_weights=True
)

# =====================================
# TRAIN MODEL
# =====================================

history = model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=256,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

# =====================================
# PREDICT
# =====================================

predictions = model.predict(
    X_test
)

predictions = target_scaler.inverse_transform(
    predictions
)

actual = target_scaler.inverse_transform(
    y_test
)

# =====================================
# EVALUATION
# =====================================

mae = mean_absolute_error(
    actual,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        actual,
        predictions
    )
)

r2 = r2_score(
    actual,
    predictions
)

print("\n====================================")
print("MULTIVARIATE LSTM RESULTS")
print("====================================")

print(
    "MAE :",
    round(mae, 2)
)

print(
    "RMSE:",
    round(rmse, 2)
)

print(
    "R²  :",
    round(r2, 4)
)

# =====================================
# SAVE MODEL
# =====================================

model.save(
    "models/multivariate_lstm.keras"
)

print(
    "\nModel Saved Successfully"
)

print(
    "models/multivariate_lstm.keras"
)

# =====================================
# SAMPLE PREDICTIONS
# =====================================

results = pd.DataFrame({

    "Actual_AQI":
        actual.flatten()[:10],

    "Predicted_AQI":
        predictions.flatten()[:10]
})

print("\nSample Predictions:")
print(results)

print(
    "\nTraining Completed Successfully!"
)