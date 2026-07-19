import streamlit as st
import pandas as pd
from pathlib import Path
import joblib
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "Processed_data" / "cleaned_nifty500.csv"
FEATURES_PATH = BASE_DIR / "Data" / "Processed_data" / "features_nifty500.csv"

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

# -----------------------
# Load Dataset
# -----------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df


@st.cache_data
def load_features():
    df = pd.read_csv(FEATURES_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df


# -----------------------
# Load ML Model
# -----------------------

MODEL_PATH = ROOT / "models" / "random_forest.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)
