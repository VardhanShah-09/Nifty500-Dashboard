import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# -----------------------
# Project Root Path
# -----------------------
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.loader import load_data
from services.live_data import get_historical_stock_data


def show():

    # -----------------------
    # Page Configuration
    # -----------------------
    st.set_page_config(
        page_title="Stock Comparison",
        layout="wide"
    )

    # -----------------------
    # Load Ticker List
    # -----------------------
    df = load_data()

    # -----------------------
    # Sidebar
    # -----------------------
    st.sidebar.title("Stock Comparison")

    stocks = sorted(df["Ticker"].unique())

    stock1 = st.sidebar.selectbox(
        "Select First Stock",
        stocks,
        index=0,
        key="comparison_stock1"
    )

    stock2 = st.sidebar.selectbox(
        "Select Second Stock",
        stocks,
        index=1,
        key="comparison_stock2"
    )

    period = st.sidebar.selectbox(
        "Select Period",
        [
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y",
            "max"
        ],
        index=5,
        key="comparison_period"
    )

    # -----------------------
    # Historical Data
    # -----------------------
    stock1_df = get_historical_stock_data(stock1, period)
    stock2_df = get_historical_stock_data(stock2, period)

    if stock1_df.empty or stock2_df.empty:
        st.warning("No historical data available.")
        st.stop()

    stock1_df = stock1_df.sort_values("Date")
    stock2_df = stock2_df.sort_values("Date")

    # Add ticker column for Plotly
    stock1_df["Ticker"] = stock1
    stock2_df["Ticker"] = stock2

    latest_stock1 = stock1_df.iloc[-1]
    latest_stock2 = stock2_df.iloc[-1]

    # -----------------------
    # Header
    # -----------------------
    st.title("📊 Stock Comparison")

    st.caption(
        "Compare the historical performance of two Nifty 500 stocks using live historical market data."
    )

    # =====================================================
    # Latest Market Values
    # =====================================================

    st.subheader("Latest Market Values")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"### {stock1}")

        st.metric(
            "Latest Close",
            f"₹{latest_stock1['Close']:.2f}"
        )

        st.metric(
            "High",
            f"₹{latest_stock1['High']:.2f}"
        )

        st.metric(
            "Low",
            f"₹{latest_stock1['Low']:.2f}"
        )

        st.metric(
            "Volume",
            f"{latest_stock1['Volume']:,.0f}"
        )

    with col2:

        st.markdown(f"### {stock2}")

        st.metric(
            "Latest Close",
            f"₹{latest_stock2['Close']:.2f}"
        )

        st.metric(
            "High",
            f"₹{latest_stock2['High']:.2f}"
        )

        st.metric(
            "Low",
            f"₹{latest_stock2['Low']:.2f}"
        )

        st.metric(
            "Volume",
            f"{latest_stock2['Volume']:,.0f}"
        )

    st.divider()

    # =====================================================
    # Closing Price Comparison
    # =====================================================

    st.subheader("Closing Price Comparison")

    comparison_df = pd.concat(
        [stock1_df, stock2_df],
        ignore_index=True
    )

    fig = px.line(
        comparison_df,
        x="Date",
        y="Close",
        color="Ticker",
        title="Closing Price Comparison"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Closing Price (₹)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Volume Comparison
    # =====================================================

    st.subheader("Trading Volume Comparison")

    fig = px.bar(
        comparison_df,
        x="Date",
        y="Volume",
        color="Ticker",
        barmode="group",
        title="Trading Volume Comparison"
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Volume"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Statistics
    # =====================================================

    st.subheader("Stock Statistics Comparison")

    stats = pd.DataFrame({

        "Statistic": [
            "Average Close",
            "Highest Close",
            "Lowest Close",
            "Average Volume",
        ],

        stock1: [
            stock1_df["Close"].mean(),
            stock1_df["Close"].max(),
            stock1_df["Close"].min(),
            stock1_df["Volume"].mean(),
        ],

        stock2: [
            stock2_df["Close"].mean(),
            stock2_df["Close"].max(),
            stock2_df["Close"].min(),
            stock2_df["Volume"].mean(),
        ],

    })

    stats[stock1] = stats[stock1].round(2)
    stats[stock2] = stats[stock2].round(2)

    st.dataframe(
        stats,
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Historical Data
    # =====================================================

    st.subheader("Historical Stock Data")

    tab1, tab2 = st.tabs([stock1, stock2])

    with tab1:

        st.dataframe(
            stock1_df,
            width="stretch",
            hide_index=True,
        )

    with tab2:

        st.dataframe(
            stock2_df,
            width="stretch",
            hide_index=True,
        )
