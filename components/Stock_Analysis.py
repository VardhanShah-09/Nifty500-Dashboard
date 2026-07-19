import streamlit as st
import sys
import pandas as pd
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.loader import load_data
import plotly.express as px
import plotly.graph_objects as go

def show():
    # -----------------------
    # Page Configuration
    # -----------------------
    st.set_page_config(
        page_title="Stock Analysis",
        layout="wide"
    )

    df = load_data()

    # -----------------------
    # Sidebar Filters
    # -----------------------
    st.sidebar.title("Stock Analysis")

    ticker = st.sidebar.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="analysis_stock"
    )

    min_date = df["Date"].min()
    max_date = df["Date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="analysis_date_range"
    )

    stock_df = df[df["Ticker"] == ticker].copy()

    if len(date_range) == 2:
        start_date, end_date = date_range

        stock_df = stock_df[
            (stock_df["Date"] >= pd.to_datetime(start_date)) &
            (stock_df["Date"] <= pd.to_datetime(end_date))
        ]

    stock_df = stock_df.sort_values("Date")

    if stock_df.empty:
        st.warning("No data available for the selected date range.")
        st.stop()

    # -----------------------
    # Stock Overview Metrics
    # -----------------------
    st.title("Stock Analysis")

    st.caption(f"Historical analysis for {ticker}")


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Current Close",
                f"₹{stock_df.iloc[-1]['Close']:.2f}")

    with col2:
        st.metric("Highest",
                f"₹{stock_df['High'].max():.2f}")

    with col3:
        st.metric("Lowest",
                f"₹{stock_df['Low'].min():.2f}")

    with col4:
        st.metric("Average Volume",
                f"{stock_df['Volume'].mean():,.0f}")
        
    # -----------------------
    # Closing Price Chart
    # -----------------------
    fig = px.line(
        stock_df,
        x="Date",
        y="Close",
        title=f"{ticker} Closing Price"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(fig,width="stretch")

    # -----------------------
    # Candlestick Chart
    # -----------------------
    fig = go.Figure(data=[
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"]
        )
    ])

    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} Candlestick Chart",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig,width="stretch")

    # -----------------------
    # Trading Volume Chart
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

    st.plotly_chart(fig, width="stretch")

    # -----------------------
    # Stock Statistics
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
    # Historical Stock Data
    # -----------------------
    st.subheader("Historical Data")

    st.dataframe(
        stock_df,
        width="stretch",
        hide_index=True
    )
