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
    # Load Dataset
    # =====================================================
    df = load_data()

    # =====================================================
    # Page Header
    # =====================================================
    st.title("Market Overview")
    st.caption(
        "Explore live market data, technical indicators, and historical trends for any Nifty500 stock."
    )

    st.divider()

    # =====================================================
    # Market Configuration
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:

        ticker = st.selectbox(
            "Select Stock",
            sorted(df["Ticker"].unique()),
            key="market_overview_stock",
        )

    with col2:

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
            key="market_overview_period",
        )

    st.divider()

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
    # Live Market
    # =====================================================
    st.subheader("Live Market")

    if live_data["success"]:

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric(
                "Current Price",
                f"₹{live_data['price']:.2f}",
            )

        with c2:
            st.metric(
                "Open",
                f"₹{live_data['open']:.2f}",
            )

        with c3:
            st.metric(
                "High",
                f"₹{live_data['high']:.2f}",
            )

        with c4:
            st.metric(
                "Low",
                f"₹{live_data['low']:.2f}",
            )

        with c5:
            st.metric(
                "Volume",
                f"{live_data['volume']:,}",
            )

        st.caption(
            f"🕒 Last Updated: {live_data['last_updated']}"
        )

    else:

        st.error(
            live_data["error"]
        )

    st.divider()

    # =====================================================
    # Technical Snapshot
    # =====================================================
    st.subheader("Technical Snapshot")

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Trend",
            trend,
        )

    with col2:
        st.metric(
            "RSI",
            f"{latest['RSI']:.2f}",
            rsi_status,
        )

    with col3:
        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}",
        )

    with col4:
        st.metric(
            "SMA20",
            f"₹{latest['SMA20']:.2f}",
        )

    st.divider()

    # =====================================================
    # Market Statistics
    # =====================================================
    st.subheader("Market Statistics")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Current Close",
            f"₹{latest['Close']:.2f}",
        )

    with s2:
        st.metric(
            "Highest Close",
            f"₹{history_df['Close'].max():.2f}",
        )

    with s3:
        st.metric(
            "Lowest Close",
            f"₹{history_df['Close'].min():.2f}",
        )

    with s4:
        st.metric(
            "Trading Days",
            len(history_df),
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
            mode="lines",
            name="Close Price",
            line=dict(width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["SMA20"],
            mode="lines",
            name="SMA20",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["SMA50"],
            mode="lines",
            name="SMA50",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=520,
        title=f"{ticker} Closing Price",
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
    # Bollinger Bands
    # =====================================================
    st.subheader("Bollinger Bands")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Close"],
            name="Close",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Upper_Band"],
            name="Upper Band",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Lower_Band"],
            name="Lower Band",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # RSI Analysis
    # =====================================================
    st.subheader("Relative Strength Index (RSI)")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["RSI"],
            mode="lines",
            name="RSI",
        )
    )

    fig.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Overbought",
    )

    fig.add_hline(
        y=30,
        line_dash="dash",
        annotation_text="Oversold",
    )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        hovermode="x unified",
        yaxis=dict(range=[0, 100]),
    )

    st.plotly_chart(
        fig,
        width="stretch",
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
            name="MACD",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history_df["Date"],
            y=history_df["Signal"],
            name="Signal",
        )
    )

    fig.add_trace(
        go.Bar(
            x=history_df["Date"],
            y=history_df["Histogram"],
            name="Histogram",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        barmode="relative",
        hovermode="x unified",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # Trading Volume
    # =====================================================
    st.subheader("Trading Volume")

    volume_fig = px.bar(
        history_df,
        x="Date",
        y="Volume",
        title=f"{ticker} Trading Volume",
    )

    volume_fig.update_layout(
        template="plotly_dark",
        height=350,
    )

    st.plotly_chart(
        volume_fig,
        width="stretch",
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

    left, right = st.columns(2)

    with left:

        st.metric(
            "Overall Return",
            f"{total_return:.2f}%",
        )

        st.metric(
            "Average Close",
            f"₹{history_df['Close'].mean():.2f}",
        )

        st.metric(
            "Highest Close",
            f"₹{history_df['Close'].max():.2f}",
        )

    with right:

        st.metric(
            "Average Volume",
            f"{history_df['Volume'].mean():,.0f}",
        )

        st.metric(
            "Maximum Volume",
            f"{history_df['Volume'].max():,.0f}",
        )

        st.metric(
            "Selected Period",
            period,
        )

    st.divider()

    # =====================================================
    # Historical Market Data
    # =====================================================
    with st.expander(
        "View Historical Market Data",
        expanded=False,
    ):

        st.dataframe(
            history_df.sort_values(
                "Date",
                ascending=False,
            ),
            width="stretch",
            hide_index=True,
        )

    st.divider()

    st.caption(
        "Live market data and historical OHLCV data are sourced from Yahoo Finance. "
        "Technical indicators are calculated from historical market prices."
    )
