# =====================================================
# Import Libraries
# =====================================================
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import (          # type: ignore
    LSTM,
    Dense,
    Dropout,
)

# =====================================================
# Paths
# =====================================================
ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "Data" / "Processed_data" / "features_nifty500.csv"

MODEL_PATH = ROOT / "models" / "lstm.keras"

# =====================================================
# Load Dataset
# =====================================================
df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape : {df.shape}")

# =====================================================
# Remove Missing Values
# =====================================================

df = df.dropna().reset_index(drop=True)

print(f"After Cleaning : {df.shape}")

# =====================================================
# Feature Selection
# =====================================================
FEATURE_COLUMNS = [

    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    "SMA20",
    "SMA50",

    "EMA12",
    "EMA26",

    "RSI",

    "MACD",
    "Signal",
    "Histogram",

    "Upper_Band",
    "Lower_Band",

]

TARGET = "Target"

# =====================================================
# Sort Dataset
# =====================================================

df = df.sort_values(
    by=["Ticker", "Date"]
).reset_index(drop=True)

# =====================================================
# Scaling
# =====================================================
feature_scaler = MinMaxScaler()

target_scaler = MinMaxScaler()

feature_scaler.fit(
    df[FEATURE_COLUMNS]
)

target_scaler.fit(
    df[[TARGET]]
)

joblib.dump(
    feature_scaler,
    ROOT / "models" / "feature_scaler.pkl"
)

joblib.dump(
    target_scaler,
    ROOT / "models" / "target_scaler.pkl"
)

print("\nScaler Saved Successfully")


# =====================================================
# Create Sequences
# =====================================================

SEQUENCE_LENGTH = 60

X = []
y = []

for ticker in df["Ticker"].unique():

    ticker_df = df[df["Ticker"] == ticker].reset_index(drop=True)

    # Skip tickers with insufficient history
    if len(ticker_df) <= SEQUENCE_LENGTH:
        continue

    # Scale using the global scalers
    scaled_features = feature_scaler.transform(
        ticker_df[FEATURE_COLUMNS]
    )

    scaled_target = target_scaler.transform(
        ticker_df[[TARGET]]
    )

    # Create sequences for this ticker only
    for i in range(SEQUENCE_LENGTH, len(ticker_df)):

        X.append(
            scaled_features[i - SEQUENCE_LENGTH:i]
        )

        y.append(
            scaled_target[i, 0]
        )

X = np.array(X)
y = np.array(y)

print(f"\nInput Shape  : {X.shape}")
print(f"Target Shape : {y.shape}")

# =====================================================
# Train Test Split
# =====================================================
split_index = int(len(X) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

print(f"\nTraining : {X_train.shape}")
print(f"Testing  : {X_test.shape}")


# =====================================================
# Build LSTM Model
# =====================================================
model = Sequential()

model.add(

    LSTM(

        units=64,

        return_sequences=True,

        input_shape=(

            X_train.shape[1],

            X_train.shape[2],

        ),
    )
)

model.add(Dropout(0.2))

model.add(LSTM(units=32,))

model.add(Dropout(0.2))

model.add(Dense(16, activation="relu",))

model.add(Dense(1,))

model.compile(
    optimizer="adam",
    loss="mean_squared_error",
    metrics=["mae"],
)

print("\nLSTM Model Created Successfully")

# =====================================================
# Train LSTM Model
# =====================================================
print("\nTraining LSTM Model...")

history = model.fit(

    X_train,
    y_train,

    validation_data=(

        X_test,
        y_test,

    ),

    epochs=20,
    batch_size=64,
    verbose=1,
)

print("\nTraining Completed.")


# =====================================================
# Model Evaluation
# =====================================================
predictions = model.predict(

    X_test,
    verbose=0,
)

predictions = predictions.flatten()


# =====================================================
# Inverse Scaling
# =====================================================
predictions = target_scaler.inverse_transform(
    predictions.reshape(-1, 1)
).flatten()

actual = target_scaler.inverse_transform(
    y_test.reshape(-1, 1)
).flatten()


# =====================================================
# Performance Metrics
# =====================================================
mae = mean_absolute_error(
    actual,
    predictions,
)

rmse = mean_squared_error(
    actual,
    predictions,
) ** 0.5

r2 = r2_score(
    actual,
    predictions,
)

print("\n==============================")
print("Model Performance")
print("==============================")

print(f"MAE  : {mae:.4f}")

print(f"RMSE : {rmse:.4f}")

print(f"R²   : {r2:.6f}")


# =====================================================
# Training History
# =====================================================
history_df = pd.DataFrame(
    history.history
)

print("\n==============================")
print("Training History")
print("==============================")
print(history_df.tail())

# =====================================================
# Save Model
# =====================================================
MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

model.save(MODEL_PATH)

print("\nModel Saved Successfully")

print(MODEL_PATH)

model_size = MODEL_PATH.stat().st_size / (1024 * 1024)

print(f"Model Size : {model_size:.2f} MB")


# =====================================================
# Sample Prediction
# =====================================================

sample = X_test[0:1]

sample_prediction = model.predict(
    sample,
    verbose=0,
).flatten()[0]

predicted_close = target_scaler.inverse_transform(
    np.array([[sample_prediction]])
)[0, 0]

actual_close = actual[0]

print("\n==============================")
print("Sample Prediction")
print("==============================")

print(f"Predicted Close : {predicted_close:.2f}")
print(f"Actual Close    : {actual_close:.2f}")


# =====================================================
# Model Summary
# =====================================================
print("\n==============================")
print("Model Summary")
print("==============================")

model.summary()


# =====================================================
# Final Summary
# =====================================================
print("\n==============================")
print("Training Completed Successfully")
print("==============================")

print(f"Dataset Shape : {df.shape}")

print(f"Training Samples : {len(X_train):,}")

print(f"Testing Samples  : {len(X_test):,}")

print(f"Sequence Length : {SEQUENCE_LENGTH}")

print(f"Features Used   : {len(FEATURE_COLUMNS)}")

print(f"Model Size      : {model_size:.2f} MB")

print(f"MAE             : {mae:.4f}")

print(f"RMSE            : {rmse:.4f}")

print(f"R² Score        : {r2:.6f}")
