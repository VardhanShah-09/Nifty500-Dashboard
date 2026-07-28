# =====================================================
# Import Libraries
# =====================================================

import time
import pandas as pd
from pathlib import Path

from xgboost import XGBRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


# =====================================================
# Paths
# =====================================================

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "Data" / "Processed_data" / "features_nifty500.csv"

MODEL_PATH = ROOT / "models" / "xgboost.json"


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

X = df[FEATURE_COLUMNS]

y = df[TARGET]


# =====================================================
# Train Test Split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    shuffle=False,

    random_state=42,

)

print(f"Training : {X_train.shape}")
print(f"Testing  : {X_test.shape}")


# =====================================================
# Train XGBoost Model
# =====================================================

model = XGBRegressor(

    objective="reg:squarederror",

    n_estimators=300,

    learning_rate=0.05,

    max_depth=8,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    n_jobs=-1,

)

print("\nTraining XGBoost Model...")

start_time = time.time()

model.fit(

    X_train,

    y_train,

)

training_time = time.time() - start_time

print("Training Completed.")


# =====================================================
# Model Evaluation
# =====================================================

predictions = model.predict(X_test)

mae = mean_absolute_error(

    y_test,

    predictions,

)

rmse = mean_squared_error(

    y_test,

    predictions,

) ** 0.5

r2 = r2_score(

    y_test,

    predictions,

)

print("\n==============================")
print("Model Performance")
print("==============================")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.6f}")

print(f"Training Time : {training_time:.2f} seconds")

# =====================================================
# Feature Importance
# =====================================================

importance = pd.DataFrame({

    "Feature": FEATURE_COLUMNS,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False,

)

print("\n==============================")
print("Feature Importance")
print("==============================")

print(importance)


# =====================================================
# Save Model
# =====================================================

MODEL_PATH.parent.mkdir(

    parents=True,

    exist_ok=True,

)

model.save_model(MODEL_PATH)

print("\nModel Saved Successfully")

print(MODEL_PATH)

model_size = MODEL_PATH.stat().st_size / (1024 * 1024)

print(f"Model Size : {model_size:.2f} MB")


# =====================================================
# Sample Prediction
# =====================================================

sample = X_test.iloc[[0]]

prediction = model.predict(sample)[0]

actual = y_test.iloc[0]

print("\n==============================")
print("Sample Prediction")
print("==============================")

print(f"Predicted Close : {prediction:.2f}")

print(f"Actual Close    : {actual:.2f}")


# =====================================================
# Save Feature Importance
# =====================================================

IMPORTANCE_PATH = ROOT / "models" / "xgboost_feature_importance.csv"

importance.to_csv(

    IMPORTANCE_PATH,

    index=False,

)

print("\nFeature Importance Saved Successfully")

print(IMPORTANCE_PATH)
