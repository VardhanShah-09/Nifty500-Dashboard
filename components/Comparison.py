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
    # Load Dataset
    # =====================================================
    df = load_data()

    # =====================================================
    # Page Header
    # =====================================================
    st.title("Stock Comparison")
    st.caption(
        "Compare the historical performance and technical indicators of two Nifty500 stocks."
    )

    st.divider()

    # =====================================================
    # Comparison Configuration
    # =====================================================
    stocks = sorted(df["Ticker"].unique())

    col1, col2, col3 = st.columns(3)

    with col1:

        stock1 = st.selectbox(
            "First Stock",
            stocks,
            index=0,
            key="comparison_stock1",
        )

    with col2:

        stock2 = st.selectbox(
            "Second Stock",
            stocks,
            index=1,
            key="comparison_stock2",
        )

    with col3:

        period = st.selectbox(
            "Time Period",
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
            key="comparison_period",
        )

    st.divider()

    # =====================================================
    # Historical Data
    # =====================================================
    stock1_df = get_historical_stock_data(
        stock1,
        period,
    )

    stock2_df = get_historical_stock_data(
        stock2,
        period,
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
        ignore_index=True,
    )

    # =====================================================
    # Latest Market Overview
    # =====================================================
    st.subheader("Latest Market Overview")

    left, right = st.columns(2)

    with left:

        st.markdown(f"### {stock1}")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Current Price",
                f"₹{latest1['Close']:.2f}",
            )

            st.metric(
                "High",
                f"₹{latest1['High']:.2f}",
            )

        with c2:

            st.metric(
                "Low",
                f"₹{latest1['Low']:.2f}",
            )

            st.metric(
                "Volume",
                f"{latest1['Volume']:,.0f}",
            )

    with right:

        st.markdown(f"### {stock2}")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Current Price",
                f"₹{latest2['Close']:.2f}",
            )

            st.metric(
                "High",
                f"₹{latest2['High']:.2f}",
            )

        with c2:

            st.metric(
                "Low",
                f"₹{latest2['Low']:.2f}",
            )

            st.metric(
                "Volume",
                f"{latest2['Volume']:,.0f}",
            )

    st.divider()

    # =====================================================
    # Technical Comparison
    # =====================================================
    st.subheader("Technical Comparison")

    left, right = st.columns(2)

    with left:

        st.markdown(f"### {stock1}")

        tc1, tc2, tc3 = st.columns(3)

        tc1.metric(
            "RSI",
            f"{latest1['RSI']:.2f}",
        )

        tc2.metric(
            "MACD",
            f"{latest1['MACD']:.2f}",
        )

        tc3.metric(
            "SMA20",
            f"₹{latest1['SMA20']:.2f}",
        )

    with right:

        st.markdown(f"### {stock2}")

        tc1, tc2, tc3 = st.columns(3)

        tc1.metric(
            "RSI",
            f"{latest2['RSI']:.2f}",
        )

        tc2.metric(
            "MACD",
            f"{latest2['MACD']:.2f}",
        )

        tc3.metric(
            "SMA20",
            f"₹{latest2['SMA20']:.2f}",
        )

    st.divider()

    # =====================================================
    # Closing Price Comparison
    # =====================================================
    st.subheader(" Closing Price Comparison")

    fig = px.line(
        comparison_df,
        x="Date",
        y="Close",
        color="Ticker",
    )

    fig.update_layout(
        template="plotly_dark",
        title="Closing Price Comparison",
        height=500,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            y=1.02,
            x=0,
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # Moving Average Comparison
    # =====================================================
    st.subheader("Moving Average Comparison")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["SMA20"],
            name=f"{stock1} SMA20",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["SMA20"],
            name=f"{stock2} SMA20",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["SMA50"],
            name=f"{stock1} SMA50",
            line=dict(dash="dot"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["SMA50"],
            name=f"{stock2} SMA50",
            line=dict(dash="dot"),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # RSI Comparison
    # =====================================================
    st.subheader("RSI Comparison")

    rsi_fig = go.Figure()

    rsi_fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["RSI"],
            name=stock1,
        )
    )

    rsi_fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["RSI"],
            name=stock2,
        )
    )

    rsi_fig.add_hline(
        y=70,
        line_dash="dash",
    )

    rsi_fig.add_hline(
        y=30,
        line_dash="dash",
    )

    rsi_fig.update_layout(
        template="plotly_dark",
        height=350,
        hovermode="x unified",
        yaxis=dict(range=[0, 100]),
    )

    st.plotly_chart(
        rsi_fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # MACD Comparison
    # =====================================================
    st.subheader("MACD Comparison")

    macd_fig = go.Figure()

    macd_fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["MACD"],
            name=f"{stock1} MACD",
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["MACD"],
            name=f"{stock2} MACD",
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=stock1_df["Date"],
            y=stock1_df["Signal"],
            name=f"{stock1} Signal",
            line=dict(dash="dot"),
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=stock2_df["Date"],
            y=stock2_df["Signal"],
            name=f"{stock2} Signal",
            line=dict(dash="dot"),
        )
    )

    macd_fig.update_layout(
        template="plotly_dark",
        height=450,
        hovermode="x unified",
    )

    st.plotly_chart(
        macd_fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # Volume Comparison
    # =====================================================
    st.subheader("Volume Comparison")

    volume_fig = px.bar(
        comparison_df,
        x="Date",
        y="Volume",
        color="Ticker",
        barmode="group",
    )

    volume_fig.update_layout(
        template="plotly_dark",
        height=450,
    )

    st.plotly_chart(
        volume_fig,
        width="stretch",
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
            round(latest1["RSI"], 2),
            round(latest1["MACD"], 2),
            round(latest1["Close"], 2),
            round(latest1["SMA20"], 2),
            round(latest1["SMA50"], 2),
        ],

        stock2: [
            get_trend(latest2),
            round(latest2["RSI"], 2),
            round(latest2["MACD"], 2),
            round(latest2["Close"], 2),
            round(latest2["SMA20"], 2),
            round(latest2["SMA50"], 2),
        ],
    })

    summary = summary.astype(str)

    st.dataframe(
        summary,
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Performance Statistics
    # =====================================================
    st.subheader("Performance Statistics")

    stats = pd.DataFrame({

        "Statistic": [
            "Average Close",
            "Highest Close",
            "Lowest Close",
            "Average Volume",
            "Trading Days",
        ],

        stock1: [
            round(stock1_df["Close"].mean(), 2),
            round(stock1_df["Close"].max(), 2),
            round(stock1_df["Close"].min(), 2),
            round(stock1_df["Volume"].mean(), 2),
            len(stock1_df),
        ],

        stock2: [
            round(stock2_df["Close"].mean(), 2),
            round(stock2_df["Close"].max(), 2),
            round(stock2_df["Close"].min(), 2),
            round(stock2_df["Volume"].mean(), 2),
            len(stock2_df),
        ],
    })

    st.dataframe(
        stats,
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Historical Market Data
    # =====================================================
    with st.expander(
        "View Historical Market Data",
        expanded=False,
    ):
        st.subheader("Historical Market Data")

        tab1, tab2 = st.tabs([stock1, stock2])

        with tab1:

            st.dataframe(
                stock1_df.sort_values(
                    "Date",
                    ascending=False,
                ),
                width="stretch",
                hide_index=True,
            )

        with tab2:

            st.dataframe(
                stock2_df.sort_values(
                    "Date",
                    ascending=False,
                ),
                width="stretch",
                hide_index=True,
            )

    st.divider()

    st.caption(
        "Historical market data is provided by Yahoo Finance. "
        "Charts and indicators are generated using the selected comparison period."
    )
