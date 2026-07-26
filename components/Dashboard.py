import streamlit as st
import sys
from pathlib import Path
from services.live_data import get_live_stock_data

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from utils.loader import load_data

def show():
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
    # Select Stock
    # -----------------------
    st.subheader("Select Stock")

    ticker = st.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="dashboard_stock"
    )
    
    # -----------------------
    # Live Market Data
    # -----------------------

    live_data = get_live_stock_data(ticker)

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

        if live_data["success"]:
            st.metric(
                "Live Price",
                f"₹{live_data['price']:.2f}"
            )
        else:
            st.metric("Live Price", "N/A")

    with col4:

        if live_data["success"]:
            st.metric(
                "Live Volume",
                f"{live_data['volume']:,}"
            )
        else:
            st.metric("Live Volume", "N/A")

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

      if live_data["success"]:
            st.metric(
                "Live Price",
                f"₹{live_data['price']:.2f}"
            )

    with col3:

        if live_data["success"]:
            st.metric(
                "Today's High",
                f"₹{live_data['high']:.2f}"
            )

    with col4:

        if live_data["success"]:
            st.metric(
                "Today's Low",
                f"₹{live_data['low']:.2f}"
            )


    st.subheader("📈 Live Market")

    if live_data["success"]:

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Price", f"₹{live_data['price']:.2f}")
        c2.metric("Open", f"₹{live_data['open']:.2f}")
        c3.metric("High", f"₹{live_data['high']:.2f}")
        c4.metric("Low", f"₹{live_data['low']:.2f}")
        c5.metric("Volume", f"{live_data['volume']:,}")

        st.caption(
            f"Last Updated : {live_data['last_updated']}"
        )

    else:

        st.error(live_data["error"])
    # -----------------------
    # Preview
    # -----------------------
    st.subheader("Selected Stock Data")

    st.dataframe(
        ticker_df.tail(15),
        width="stretch",
        hide_index=True
    )
