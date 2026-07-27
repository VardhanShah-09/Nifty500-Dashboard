import streamlit as st
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
from services.live_data import (
    get_live_stock_data,
    get_historical_stock_data,
)



def show():

    # =====================================================
    # Page Configuration
    # =====================================================

    st.set_page_config(
        page_title="Market Overview",
        layout="wide"
    )

    # =====================================================
    # Load Ticker List
    # =====================================================

    df = load_data()

    # =====================================================
    # Sidebar
    # =====================================================

    st.sidebar.title("Market Overview")

    ticker = st.sidebar.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="market_overview_stock",
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
        key="market_overview_period",
    )

    # =====================================================
    # Fetch Data
    # =====================================================

    live_data = get_live_stock_data(ticker)

    history_df = get_historical_stock_data(
        ticker,
        period,
    )

    if history_df.empty:
        st.warning("No historical data available.")
        st.stop()

    history_df = history_df.sort_values("Date")

    latest = history_df.iloc[-1]

    # =====================================================
    # Header
    # =====================================================

    st.title("📈 Market Overview")

    st.caption(
        "Real-time market overview powered by Yahoo Finance."
    )

    # =====================================================
    # Live Market
    # =====================================================

    st.subheader("Live Market")

    if live_data["success"]:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Live Price",
                f"₹{live_data['price']:.2f}"
            )

        with col2:
            st.metric(
                "Open",
                f"₹{live_data['open']:.2f}"
            )

        with col3:
            st.metric(
                "High",
                f"₹{live_data['high']:.2f}"
            )

        with col4:
            st.metric(
                "Low",
                f"₹{live_data['low']:.2f}"
            )

        with col5:
            st.metric(
                "Volume",
                f"{live_data['volume']:,}"
            )

        st.caption(
            f"Last Updated : {live_data['last_updated']}"
        )

    else:

        st.error(live_data["error"])

    st.divider()
    
    # =====================================================
    # Technical Snapshot
    # =====================================================

    st.subheader("Technical Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    if latest["Close"] > latest["SMA20"] > latest["SMA50"]:
        trend = "🟢 Bullish"

    elif latest["Close"] < latest["SMA20"] < latest["SMA50"]:
        trend = "🔴 Bearish"

    else:
        trend = "🟡 Sideways"


    if latest["RSI"] > 70:
        rsi_status = "Overbought"

    elif latest["RSI"] < 30:
        rsi_status = "Oversold"

    else:
        rsi_status = "Neutral"


    with col1:
        st.metric(
            "RSI",
            f"{latest['RSI']:.2f}",
            rsi_status
        )

    with col2:
        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}"
        )

    with col3:
        st.metric(
            "Trend",
            trend
        )

    with col4:
        st.metric(
            "SMA20",
            f"₹{latest['SMA20']:.2f}"
        )

    st.divider()

    # =====================================================
    # Market Statistics
    # =====================================================

    st.subheader("Market Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Current Close",
            f"₹{latest['Close']:.2f}"
        )

    with col2:

        st.metric(
            "Highest Close",
            f"₹{history_df['Close'].max():.2f}"
        )

    with col3:

        st.metric(
            "Lowest Close",
            f"₹{history_df['Close'].min():.2f}"
        )

    with col4:

        st.metric(
            "Trading Days",
            len(history_df)
        )

    st.divider()

    # =====================================================
    # Closing Price Trend
    # =====================================================

    st.subheader("Closing Price Trend")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["SMA20"],
            name="SMA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["SMA50"],
            name="SMA50"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        title=f"{ticker} Price Trend"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Bollinger Bands
    # =====================================================

    st.subheader("Bollinger Bands")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Upper_Band"],
            name="Upper Band"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Lower_Band"],
            name="Lower Band"
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
    # RSI
    # =====================================================

    st.subheader("Relative Strength Index (RSI)")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["RSI"],
            name="RSI",
            mode="lines"
        )
    )

    fig.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Overbought"
    )

    fig.add_hline(
        y=30,
        line_dash="dash",
        annotation_text="Oversold"
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
    # MACD
    # =====================================================

    st.subheader("MACD")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["MACD"],
            name="MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Signal"],
            name="Signal"
        )
    )

    fig.add_trace(
        go.Bar(
            x=history_df["Date"],
            y=history_df["Histogram"],
            name="Histogram"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        barmode="relative"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Trading Volume
    # =====================================================

    st.subheader("Trading Volume")

    fig = px.bar(
        history_df,
        x="Date",
        y="Volume",
        title=f"{ticker} Trading Volume"
    )

    fig.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Performance Summary
    # =====================================================

    st.subheader("Performance Summary")

    first_close = history_df.iloc[0]["Close"]
    last_close = history_df.iloc[-1]["Close"]

    total_return = (
        (last_close - first_close)
        / first_close
    ) * 100

    if latest["Close"] > latest["SMA20"] > latest["SMA50"]:
        trend = "🟢 Bullish"

    elif latest["Close"] < latest["SMA20"] < latest["SMA50"]:
        trend = "🔴 Bearish"

    else:
        trend = "🟡 Sideways"

    left, right = st.columns(2)

    with left:

        st.success("Market Trend")

        st.write(f"**Trend :** {trend}")

        st.write(
            f"**Overall Return :** {total_return:.2f}%"
        )

        st.write(
            f"**Current Close :** ₹{latest['Close']:.2f}"
        )

        st.write(
            f"**SMA20 :** ₹{latest['SMA20']:.2f}"
        )

        st.write(
            f"**SMA50 :** ₹{latest['SMA50']:.2f}"
        )

    with right:

        st.info("Momentum")

        st.write(
            f"**RSI :** {latest['RSI']:.2f}"
        )

        st.write(
            f"**MACD :** {latest['MACD']:.2f}"
        )

        st.write(
            f"**Signal :** {latest['Signal']:.2f}"
        )

        st.write(
            f"**Histogram :** {latest['Histogram']:.2f}"
        )

    st.divider()

    # =====================================================
    # Historical Statistics
    # =====================================================

    st.subheader("Historical Statistics")

    stat1, stat2 = st.columns(2)

    with stat1:

        st.write(
            f"Highest Close : ₹{history_df['Close'].max():.2f}"
        )

        st.write(
            f"Lowest Close : ₹{history_df['Close'].min():.2f}"
        )

        st.write(
            f"Average Close : ₹{history_df['Close'].mean():.2f}"
        )

        st.write(
            f"Highest Volume : {history_df['Volume'].max():,.0f}"
        )

    with stat2:

        st.write(
            f"Average Volume : {history_df['Volume'].mean():,.0f}"
        )

        st.write(
            f"Trading Days : {len(history_df)}"
        )

        st.write(
            f"Selected Period : {period}"
        )

        st.write(
            f"Selected Stock : {ticker}"
        )

    st.divider()

    # =====================================================
    # Recent Market Data
    # =====================================================

    st.subheader("Recent Market Data")

    with st.expander(
        "View Recent Historical Data",
        expanded=False
    ):

        st.dataframe(
            history_df.tail(20),
            width="stretch",
            hide_index=True
        )

    st.divider()

    # =====================================================
    # Data Information
    # =====================================================

    st.subheader("Data Information")

    c1, c2, c3 = st.columns(3)

    c1.info(
        f"**Stock**\n\n{ticker}"
    )

    c2.info(
        f"**Period**\n\n{period}"
    )

    c3.info(
        "**Source**\n\nYahoo Finance"
    )

    st.divider()

    # =====================================================
    # Footer
    # =====================================================

    st.success(
        "Market Overview loaded successfully using live Yahoo Finance data."
    )
