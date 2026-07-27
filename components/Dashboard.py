import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go

from services.live_data import (
    get_live_stock_data,
    get_historical_stock_data,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from utils.loader import load_data


def show():

    # =====================================================
    # Page Configuration
    # =====================================================
    st.set_page_config(
        page_title="Dashboard",
        layout="wide"
    )

    # =====================================================
    # Load Dataset
    # =====================================================
    df = load_data()

    # =====================================================
    # Stock Selection
    # =====================================================
    st.subheader("Select Stock")

    ticker = st.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="dashboard_stock"
    )

    # Dataset for Selected Stock
    ticker_df = df[df["Ticker"] == ticker]

    # =====================================================
    # Live Market Data
    # =====================================================
    live_data = get_live_stock_data(ticker)

    # =====================================================
    # Historical Market Data
    # =====================================================
    historical_data = get_historical_stock_data(
        ticker,
        period="1y"
    )

    if historical_data.empty:
        st.error("Unable to load historical data.")
        st.stop()

    # =====================================================
    # Latest Technical Values
    # =====================================================
    latest = historical_data.iloc[-1]

    # =====================================================
    # Header
    # =====================================================
    st.title("📈 Nifty500 Analytics Dashboard")

    st.caption(
        "Machine Learning Based Stock Market Analytics Platform"
    )

    # =====================================================
    # Market Overview
    # =====================================================
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
            st.metric(
                "Live Price",
                "N/A"
            )

    with col4:

        if live_data["success"]:
            st.metric(
                "Live Volume",
                f"{live_data['volume']:,}"
            )
        else:
            st.metric(
                "Live Volume",
                "N/A"
            )

    st.divider()

    # =====================================================
    # Technical Snapshot
    # =====================================================
    st.subheader("Technical Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    # Trend Detection
    if latest["Close"] > latest["SMA20"] > latest["SMA50"]:
        trend = "🟢 Bullish"

    elif latest["Close"] < latest["SMA20"] < latest["SMA50"]:
        trend = "🔴 Bearish"

    else:
        trend = "🟡 Sideways"

    # RSI Status
    if latest["RSI"] > 70:
        rsi_status = "Overbought"

    elif latest["RSI"] < 30:
        rsi_status = "Oversold"

    else:
        rsi_status = "Neutral"

    with c1:
        st.metric(
            "RSI",
            f"{latest['RSI']:.2f}",
            rsi_status
        )

    with c2:
        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}"
        )

    with c3:
        st.metric(
            "Trend",
            trend
        )

    with c4:
        st.metric(
            "SMA20",
            f"₹{latest['SMA20']:.2f}"
        )

    st.divider()
    
        # =====================================================
    # Market Summary
    # =====================================================
    st.subheader("Market Summary")

    left, right = st.columns(2)

    with left:
        st.write(f"**Highest Close Price :** ₹{df['Close'].max():.2f}")
        st.write(f"**Lowest Close Price :** ₹{df['Close'].min():.2f}")
        st.write(f"**Trading Days :** {df['Date'].nunique()}")

    with right:
        st.write(f"**Stocks Covered :** {df['Ticker'].nunique()}")
        st.write(f"**First Date :** {df['Date'].min().date()}")
        st.write(f"**Last Date :** {df['Date'].max().date()}")

    st.divider()

    # =====================================================
    # Recent Market Data
    # =====================================================
    st.subheader("Recent Market Data")

    st.dataframe(
        ticker_df.tail(10),
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Live Market
    # =====================================================
    st.subheader("📈 Live Market")

    if live_data["success"]:

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Price",
            f"₹{live_data['price']:.2f}"
        )

        c2.metric(
            "Open",
            f"₹{live_data['open']:.2f}"
        )

        c3.metric(
            "High",
            f"₹{live_data['high']:.2f}"
        )

        c4.metric(
            "Low",
            f"₹{live_data['low']:.2f}"
        )

        c5.metric(
            "Volume",
            f"{live_data['volume']:,}"
        )

        st.caption(
            f"Last Updated : {live_data['last_updated']}"
        )

    else:

        st.error(
            live_data["error"]
        )

    st.divider()

    # =====================================================
    # Price Trend
    # =====================================================
    st.subheader("Price Trend")

    fig = go.Figure()

    # Closing Price
    fig.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["Close"],
            mode="lines",
            name="Close",
            line=dict(width=3)
        )
    )

    # SMA20
    fig.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["SMA20"],
            mode="lines",
            name="SMA20"
        )
    )

    # SMA50
    fig.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["SMA50"],
            mode="lines",
            name="SMA50"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        title=f"{ticker} Price Trend",
        legend=dict(
            orientation="h",
            y=1.02,
            x=0
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # =====================================================
    # Selected Stock Statistics
    # =====================================================
    st.subheader("Selected Stock Statistics")

    stat1, stat2, stat3, stat4 = st.columns(4)

    stat1.metric(
        "Records",
        len(ticker_df)
    )

    stat2.metric(
        "Highest Close",
        f"₹{ticker_df['Close'].max():.2f}"
    )

    stat3.metric(
        "Lowest Close",
        f"₹{ticker_df['Close'].min():.2f}"
    )

    stat4.metric(
        "Average Close",
        f"₹{ticker_df['Close'].mean():.2f}"
    )

    st.divider()

    # =====================================================
    # Selected Stock Data
    # =====================================================
    with st.expander(
        "View Selected Stock Data",
        expanded=False
    ):

        st.dataframe(
            ticker_df.tail(15),
            width="stretch",
            hide_index=True,
        )
