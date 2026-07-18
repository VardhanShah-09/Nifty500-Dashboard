import streamlit as st
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "Data" / "Processed_data" / "cleaned_nifty500.csv"
FEATURES_PATH = BASE_DIR / "Data" / "Processed_data" / "features_nifty500.csv"

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
