from pathlib import Path

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
import xgboost as xgb


# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[1]

MODELS = ROOT / "models"


# ==========================================================
# Feature Columns
# ==========================================================

RF_XGB_FEATURES = [
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

LSTM_FEATURES = [
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

SEQUENCE_LENGTH = 60


# ==========================================================
# Load Random Forest
# ==========================================================

@st.cache_resource
def load_random_forest():

    return joblib.load(
        MODELS / "random_forest.pkl"
    )


# ==========================================================
# Load XGBoost
# ==========================================================

@st.cache_resource
def load_xgboost():

    model = xgb.XGBRegressor()

    model.load_model(
        MODELS / "xgboost.json"
    )

    return model


# ==========================================================
# Load LSTM
# ==========================================================

@st.cache_resource
def load_lstm():

    return tf.keras.models.load_model(
        MODELS / "lstm.keras"
    )


# ==========================================================
# Load Scalers
# ==========================================================

@st.cache_resource
def load_feature_scaler():

    return joblib.load(
        MODELS / "feature_scaler.pkl"
    )


@st.cache_resource
def load_target_scaler():

    return joblib.load(
        MODELS / "target_scaler.pkl"
    )

# ==========================================================
# Random Forest Prediction
# ==========================================================

def predict_random_forest(latest):

    model = load_random_forest()

    X = pd.DataFrame([{
        feature: latest[feature]
        for feature in RF_XGB_FEATURES
    }])

    prediction = model.predict(X)[0]

    return float(prediction)


# ==========================================================
# XGBoost Prediction
# ==========================================================

def predict_xgboost(latest):

    model = load_xgboost()

    X = pd.DataFrame([{
        feature: latest[feature]
        for feature in RF_XGB_FEATURES
    }])

    prediction = model.predict(X)[0]

    return float(prediction)


# ==========================================================
# LSTM Prediction
# ==========================================================

def predict_lstm(history):

    if len(history) < SEQUENCE_LENGTH:
        raise ValueError(
            f"LSTM requires at least {SEQUENCE_LENGTH} trading days."
        )

    model = load_lstm()

    feature_scaler = load_feature_scaler()

    target_scaler = load_target_scaler()

    sequence = history[LSTM_FEATURES].tail(SEQUENCE_LENGTH)

    sequence = feature_scaler.transform(sequence)

    sequence = np.expand_dims(
        sequence,
        axis=0
    )

    prediction = model.predict(
        sequence,
        verbose=0
    )[0][0]

    prediction = target_scaler.inverse_transform(
        [[prediction]]
    )[0][0]

    return float(prediction)


# ==========================================================
# Common Prediction Interface
# ==========================================================

def predict_stock(model_name, latest=None, history=None):

    model_name = model_name.lower()

    if model_name == "random forest":

        return predict_random_forest(latest)

    elif model_name == "xgboost":

        return predict_xgboost(latest)

    elif model_name == "lstm":

        if history is None:
            raise ValueError(
                "History dataframe is required for LSTM prediction."
            )

        return predict_lstm(history)

    else:

        raise ValueError(
            f"Unknown model: {model_name}"
        )
