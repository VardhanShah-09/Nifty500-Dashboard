import streamlit as st
import plotly.express as px
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

    fig = px.line(
        history_df,
        x="Date",
        y="Close",
        title=f"{ticker} Closing Price",
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Closing Price (₹)",
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

    fig = px.bar(
        history_df,
        x="Date",
        y="Volume",
        title=f"{ticker} Trading Volume",
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Volume",
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # Historical Statistics
    # =====================================================

    st.subheader("Historical Statistics")

    left, right = st.columns(2)

    with left:

        st.write(
            f"Highest Close : ₹{history_df['Close'].max():.2f}"
        )

        st.write(
            f"Lowest Close : ₹{history_df['Close'].min():.2f}"
        )

        st.write(
            f"Average Close : ₹{history_df['Close'].mean():.2f}"
        )

    with right:

        st.write(
            f"Average Volume : {history_df['Volume'].mean():,.0f}"
        )

        st.write(
            f"Trading Days : {len(history_df)}"
        )

        st.write(
            f"Selected Stock : {ticker}"
        )
        
        st.divider()

    # =====================================================
    # 52 Week Summary
    # =====================================================

    st.subheader("52 Week Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "52 Week High",
            f"₹{history_df['High'].max():.2f}"
        )

    with col2:

        st.metric(
            "52 Week Low",
            f"₹{history_df['Low'].min():.2f}"
        )

    with col3:

        st.metric(
            "Average High",
            f"₹{history_df['High'].mean():.2f}"
        )

    with col4:

        st.metric(
            "Average Low",
            f"₹{history_df['Low'].mean():.2f}"
        )

    st.divider()

    # =====================================================
    # Recent Market Data
    # =====================================================

    st.subheader("Recent Market Data")

    recent_df = (
        history_df.sort_values("Date", ascending=False)
        .head(20)
        .reset_index(drop=True)
    )

    st.dataframe(
        recent_df,
        width="stretch",
        hide_index=True,
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

    highest_volume = history_df["Volume"].max()
    average_volume = history_df["Volume"].mean()

    left, right = st.columns(2)

    with left:

        st.write(
            f"Opening Price (First Trading Day): ₹{history_df.iloc[0]['Open']:.2f}"
        )

        st.write(
            f"Closing Price (Latest): ₹{last_close:.2f}"
        )

        st.write(
            f"Overall Return: {total_return:.2f}%"
        )

    with right:

        st.write(
            f"Highest Trading Volume: {highest_volume:,.0f}"
        )

        st.write(
            f"Average Trading Volume: {average_volume:,.0f}"
        )

        st.write(
            f"Historical Records: {len(history_df)}"
        )

    st.divider()

    # =====================================================
    # Data Information
    # =====================================================

    st.subheader("Data Information")

    info1, info2, info3 = st.columns(3)

    with info1:

        st.info(
            f"""
**Selected Stock**

{ticker}
"""
        )

    with info2:

        st.info(
            f"""
        **Selected Period**

        {period}
        """
        )

    with info3:

        st.info(
            f"""
        **Data Source**

        Yahoo Finance
        """
        )

    st.divider()

    # =====================================================
    # Footer
    # =====================================================

    st.success(
        "Market Overview loaded successfully using live historical data from Yahoo Finance."
    )
