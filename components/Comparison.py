import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# =====================================================
# Project Root
# =====================================================
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.loader import load_data
from services.live_data import get_historical_stock_data


def show():

    # =====================================================
    # Page Configuration
    # =====================================================
    st.set_page_config(
        page_title="Stock Comparison",
        layout="wide"
    )

    # =====================================================
    # Load Stock List
    # =====================================================
    df = load_data()

    # =====================================================
    # Sidebar
    # =====================================================
    st.sidebar.title("📊 Stock Comparison")

    stocks = sorted(df["Ticker"].unique())

    stock1 = st.sidebar.selectbox(
        "First Stock",
        stocks,
        index=0,
        key="comparison_stock1"
    )

    stock2 = st.sidebar.selectbox(
        "Second Stock",
        stocks,
        index=1,
        key="comparison_stock2"
    )

    period = st.sidebar.selectbox(
        "Time Period",
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

    # =====================================================
    # Historical Data
    # =====================================================
    stock1_df = get_historical_stock_data(
        stock1,
        period
    )

    stock2_df = get_historical_stock_data(
        stock2,
        period
    )

    if stock1_df.empty or stock2_df.empty:
        st.error("Historical data unavailable.")
        st.stop()

    stock1_df = stock1_df.sort_values("Date")
    stock2_df = stock2_df.sort_values("Date")

    stock1_df["Ticker"] = stock1
    stock2_df["Ticker"] = stock2

    latest1 = stock1_df.iloc[-1]
    latest2 = stock2_df.iloc[-1]

    comparison_df = pd.concat(
        [stock1_df, stock2_df],
        ignore_index=True
    )

    # =====================================================
    # Header
    # =====================================================
    st.title("📊 Stock Comparison")

    st.caption(
        "Compare technical indicators and historical performance."
    )

    # =====================================================
    # Latest Market Metrics
    # =====================================================
    st.subheader("Latest Market Metrics")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(f"### {stock1}")

        st.metric(
            "Close",
            f"₹{latest1['Close']:.2f}"
        )

        st.metric(
            "High",
            f"₹{latest1['High']:.2f}"
        )

        st.metric(
            "Low",
            f"₹{latest1['Low']:.2f}"
        )

        st.metric(
            "Volume",
            f"{latest1['Volume']:,.0f}"
        )

    with c2:

        st.markdown(f"### {stock2}")

        st.metric(
            "Close",
            f"₹{latest2['Close']:.2f}"
        )

        st.metric(
            "High",
            f"₹{latest2['High']:.2f}"
        )

        st.metric(
            "Low",
            f"₹{latest2['Low']:.2f}"
        )

        st.metric(
            "Volume",
            f"{latest2['Volume']:,.0f}"
        )

    st.divider()

    # =====================================================
    # Technical Comparison
    # =====================================================
    st.subheader("Technical Indicator Comparison")

    tc1, tc2 = st.columns(2)

    with tc1:

        st.metric(
            "RSI",
            f"{latest1['RSI']:.2f}"
        )

        st.metric(
            "MACD",
            f"{latest1['MACD']:.2f}"
        )

        st.metric(
            "SMA20",
            f"₹{latest1['SMA20']:.2f}"
        )

    with tc2:

        st.metric(
            "RSI",
            f"{latest2['RSI']:.2f}"
        )

        st.metric(
            "MACD",
            f"{latest2['MACD']:.2f}"
        )

        st.metric(
            "SMA20",
            f"₹{latest2['SMA20']:.2f}"
        )

    st.divider()

    # =====================================================
    # Closing Price Comparison
    # =====================================================
    st.subheader("Closing Price Comparison")

    fig = px.line(
        comparison_df,
        x="Date",
        y="Close",
        color="Ticker"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # =====================================================
    # SMA Comparison
    # =====================================================
    st.subheader("Moving Average Comparison")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["SMA20"],
            name=f"{stock1} SMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["SMA20"],
            name=f"{stock2} SMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["SMA50"],
            name=f"{stock1} SMA50",
            line=dict(dash="dot")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["SMA50"],
            name=f"{stock2} SMA50",
            line=dict(dash="dot")
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # =====================================================
    # Bollinger Band Comparison
    # =====================================================
    st.subheader("Bollinger Bands")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["Upper_Band"],
            name=f"{stock1} Upper"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["Lower_Band"],
            name=f"{stock1} Lower"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["Upper_Band"],
            name=f"{stock2} Upper"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["Lower_Band"],
            name=f"{stock2} Lower"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()
    # =====================================================
    # RSI Comparison
    # =====================================================
    st.subheader("RSI Comparison")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["RSI"],
            name=stock1
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["RSI"],
            name=stock2
        )
    )

    fig.add_hline(
        y=70,
        line_dash="dash"
    )

    fig.add_hline(
        y=30,
        line_dash="dash"
    )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # MACD Comparison
    # =====================================================
    st.subheader("MACD Comparison")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["MACD"],
            name=f"{stock1} MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["MACD"],
            name=f"{stock2} MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["Signal"],
            name=f"{stock1} Signal",
            line=dict(dash="dot")
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["Signal"],
            name=f"{stock2} Signal",
            line=dict(dash="dot")
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
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
        barmode="group"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Technical Summary
    # =====================================================
    st.subheader("Technical Summary")

    def get_trend(data):

        if data["Close"] > data["SMA20"] > data["SMA50"]:
            return "🟢 Bullish"

        elif data["Close"] < data["SMA20"] < data["SMA50"]:
            return "🔴 Bearish"

        return "🟡 Sideways"


    summary = pd.DataFrame({

        "Indicator": [

            "Trend",

            "RSI",

            "MACD",

            "Close",

            "SMA20",

            "SMA50",

        ],

        stock1: [

            get_trend(latest1),

            round(latest1["RSI"],2),

            round(latest1["MACD"],2),

            round(latest1["Close"],2),

            round(latest1["SMA20"],2),

            round(latest1["SMA50"],2),

        ],

        stock2: [

            get_trend(latest2),

            round(latest2["RSI"],2),

            round(latest2["MACD"],2),

            round(latest2["Close"],2),

            round(latest2["SMA20"],2),

            round(latest2["SMA50"],2),

        ]

    })

    summary = summary.astype(str)

    st.dataframe(
        summary,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # =====================================================
    # Statistics
    # =====================================================
    st.subheader("Statistics")

    stats = pd.DataFrame({

        "Statistic":[

            "Average Close",

            "Highest Close",

            "Lowest Close",

            "Average Volume",

            "Trading Days",

        ],

        stock1:[

            round(stock1_df["Close"].mean(),2),

            round(stock1_df["Close"].max(),2),

            round(stock1_df["Close"].min(),2),

            round(stock1_df["Volume"].mean(),2),

            len(stock1_df)

        ],

        stock2:[

            round(stock2_df["Close"].mean(),2),

            round(stock2_df["Close"].max(),2),

            round(stock2_df["Close"].min(),2),

            round(stock2_df["Volume"].mean(),2),

            len(stock2_df)

        ]

    })

    st.dataframe(
        stats,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # =====================================================
    # Historical Data
    # =====================================================
    st.subheader("Historical Data")

    tab1, tab2 = st.tabs([stock1, stock2])

    with tab1:

        st.dataframe(
            stock1_df,
            width="stretch",
            hide_index=True
        )

    with tab2:

        st.dataframe(
            stock2_df,
            width="stretch",
            hide_index=True
        )
