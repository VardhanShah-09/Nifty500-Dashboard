import streamlit as st
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from utils.loader import load_data

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# -----------------------
# Load Dataset
# -----------------------
df = load_data()

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("Nifty500 Dashboard")

ticker = st.sidebar.selectbox(
    "Select Stock",
    sorted(df["Ticker"].unique())
)

st.sidebar.markdown("---")

st.sidebar.success("Random Forest Model Loaded")

# -----------------------
# Header
# -----------------------
st.title("Nifty500 Analytics Dashboard")

st.caption("Machine Learning Based Stock Market Analytics Platform")

# -----------------------
# Metrics
# -----------------------
st.subheader("Market Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Stocks",
        df["Ticker"].nunique()
    )

with col2:
    st.metric(
        "Records",
        f"{len(df):,}"
    )

with col3:
    st.metric(
        "Average Close",
        f"₹{df['Close'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Volume",
        f"{df['Volume'].mean():,.0f}"
    )

# -----------------------
# Market Summary
# -----------------------
st.subheader("Market Summary")

left, right = st.columns(2)

with left:
    st.write(f"Highest Close Price: ₹{df['Close'].max():.2f}")
    st.write(f"Lowest Close Price: ₹{df['Close'].min():.2f}")
    st.write(f"Trading Days: {df['Date'].nunique()}")

with right:
    st.write(f"Stocks Covered: {df['Ticker'].nunique()}")
    st.write(f"First Date: {df['Date'].min().date()}")
    st.write(f"Last Date: {df['Date'].max().date()}")

# --------------------------
# Recent Market Data
# --------------------------
st.subheader("Recent Market Data")

st.dataframe(
    df.tail(20),
    width="stretch",
    hide_index=True
)

# -----------------------
# Dataset Statistics
# -----------------------
st.subheader("Selected Stock")

ticker_df = df[df["Ticker"] == ticker]
col1, col2, col3, col4 =  st.columns([1, 1, 1, 1])

with col1:
    st.metric("Records", len(ticker_df))

with col2:
    st.metric(
        "Latest Close",
        f"₹{ticker_df.iloc[-1]['Close']:.2f}"
    )

with col3:
    st.metric(
        "Highest",
        f"₹{ticker_df['High'].max():.2f}"
    )

with col4:
    st.metric(
        "Lowest",
        f"₹{ticker_df['Low'].min():.2f}"
    )

# -----------------------
# Preview
# -----------------------
st.subheader("Selected Stock Data")

st.dataframe(
    ticker_df.tail(15),
    width="stretch",
    hide_index=True
)
