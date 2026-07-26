import streamlit as st
import sys
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.loader import load_data
from services.live_data import get_historical_stock_data


def show():

    # -----------------------
    # Page Configuration
    # -----------------------
    st.set_page_config(
        page_title="Stock Analysis",
        layout="wide"
    )

    # -----------------------
    # Load ticker list only
    # -----------------------
    df = load_data()

    # -----------------------
    # Sidebar
    # -----------------------
    st.sidebar.title("Stock Analysis")

    ticker = st.sidebar.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="analysis_stock"
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
            "max",
        ],
        index=5,
        key="analysis_period"
    )

    # -----------------------
    # Fetch Historical Data
    # -----------------------
    stock_df = get_historical_stock_data(
        ticker,
        period,
    )

    if stock_df.empty:
        st.warning("No historical data available.")
        st.stop()

    stock_df = stock_df.sort_values("Date")

    # -----------------------
    # Header
    # -----------------------
    st.title("📈 Stock Analysis")

    st.caption(f"Historical analysis for {ticker}")

    # -----------------------
    # Metrics
    # -----------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Close",
            f"₹{stock_df.iloc[-1]['Close']:.2f}"
        )

    with col2:
        st.metric(
            "Highest",
            f"₹{stock_df['High'].max():.2f}"
        )

    with col3:
        st.metric(
            "Lowest",
            f"₹{stock_df['Low'].min():.2f}"
        )

    with col4:
        st.metric(
            "Average Volume",
            f"{stock_df['Volume'].mean():,.0f}"
        )

    # -----------------------
    # Closing Price Chart
    # -----------------------
    fig = px.line(
        stock_df,
        x="Date",
        y="Close",
        title=f"{ticker} Closing Price"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # -----------------------
    # Candlestick Chart
    # -----------------------
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=stock_df["Date"],
                open=stock_df["Open"],
                high=stock_df["High"],
                low=stock_df["Low"],
                close=stock_df["Close"],
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} Candlestick Chart",
        xaxis_rangeslider_visible=False,
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # -----------------------
    # Volume Chart
    # -----------------------
    fig = px.bar(
        stock_df,
        x="Date",
        y="Volume",
        title="Trading Volume Over Time"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # -----------------------
    # Statistics
    # -----------------------
    st.subheader("Stock Statistics")

    left, right = st.columns(2)

    with left:
        st.write(f"Highest Close : ₹{stock_df['Close'].max():.2f}")
        st.write(f"Lowest Close : ₹{stock_df['Close'].min():.2f}")
        st.write(f"Average Close : ₹{stock_df['Close'].mean():.2f}")

    with right:
        st.write(f"Trading Days : {len(stock_df)}")
        st.write(f"Average Volume : {stock_df['Volume'].mean():,.0f}")

    # -----------------------
    # Historical Data
    # -----------------------
    st.subheader("Historical Data")

    st.dataframe(
        stock_df,
        width="stretch",
        hide_index=True,
    )
