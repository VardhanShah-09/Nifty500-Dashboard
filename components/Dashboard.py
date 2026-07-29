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
    st.set_page_config(layout="wide",)
    # =====================================================
    # Load Dataset
    # =====================================================
    df = load_data()

    # =====================================================
    # Dashboard Header
    # =====================================================
    col1, col2 = st.columns([5, 1])

    with col1:
        st.title("Nifty500 Dashboard")
        st.caption(
            "Real-time NSE Stock Analytics & Machine Learning Insights"
        )

    st.divider()

    # =====================================================
    # Stock Selection
    # =====================================================
    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("Stock Selection")

        ticker = st.selectbox(
            "Choose an NSE Stock",
            sorted(df["Ticker"].unique()),
            key="dashboard_stock",
        )

    # =====================================================
    # Selected Stock Data
    # =====================================================
    ticker_df = df[df["Ticker"] == ticker]

    # =====================================================
    # Live Data
    # =====================================================
    live_data = get_live_stock_data(ticker)

    # =====================================================
    # Historical Data
    # =====================================================
    historical_data = get_historical_stock_data(
        ticker,
        period="1y",
    )

    if historical_data.empty:
        st.error("Unable to load historical data.")
        st.stop()

    latest = historical_data.iloc[-1]

    st.divider()
    
    # =====================================================
    # Dashboard Summary
    # =====================================================
    st.subheader("Dashboard Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Stocks",
            df["Ticker"].nunique(),
        )

    with col2:
        st.metric(
            "Dataset Records",
            f"{len(df):,}",
        )

    with col3:

        if live_data["success"]:
            st.metric(
                "Current Price",
                f"₹{live_data['price']:.2f}",
            )
        else:
            st.metric(
                "Current Price",
                "N/A",
            )

    with col4:

        if live_data["success"]:
            st.metric(
                "Today's Volume",
                f"{live_data['volume']:,}",
            )
        else:
            st.metric(
                "Today's Volume",
                "N/A",
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
        signal = "Overbought"
    elif latest["RSI"] < 30:
        signal = "Oversold"
    else:
        signal = "Neutral"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Trend",
            trend,
        )

    with c2:
        st.metric(
            "RSI",
            f"{latest['RSI']:.2f}",
            signal,
        )

    with c3:
        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}",
        )

    with c4:
        st.metric(
            "Signal",
            signal,
        )

    st.divider()

    # =====================================================
    # Live Market
    # =====================================================
    st.subheader("Live Market")

    if live_data["success"]:

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Current",
            f"₹{live_data['price']:.2f}",
        )

        c2.metric(
            "Open",
            f"₹{live_data['open']:.2f}",
        )

        c3.metric(
            "High",
            f"₹{live_data['high']:.2f}",
        )

        c4.metric(
            "Low",
            f"₹{live_data['low']:.2f}",
        )

        c5.metric(
            "Volume",
            f"{live_data['volume']:,}",
        )

        st.caption(
            f"Last Updated : {live_data['last_updated']}"
        )

    else:
        st.error(live_data["error"])

    st.divider()

    # =====================================================
    # Price Trend
    # =====================================================
    st.subheader("Price Trend")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["Close"],
            mode="lines",
            name="Close Price",
            line=dict(width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["SMA20"],
            mode="lines",
            name="SMA 20",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=historical_data["Date"],
            y=historical_data["SMA50"],
            mode="lines",
            name="SMA 50",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"{ticker} Price Trend (1 Year)",
        height=520,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        legend=dict(
            orientation="h",
            y=1.05,
            x=0,
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        width='stretch',
    )

    st.divider()
    
    # =====================================================
    # Recent Trading Sessions
    # =====================================================
    st.subheader("Recent Trading Sessions")

    recent_columns = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    st.dataframe(
        historical_data[recent_columns]
        .sort_values("Date", ascending=False)
        .head(10),
        width='stretch',
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Performance Statistics
    # =====================================================
    st.subheader("Performance Statistics")

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.metric(
            "Trading Records",
            f"{len(ticker_df):,}",
        )

    with stat2:
        st.metric(
            "Highest Close",
            f"₹{ticker_df['Close'].max():.2f}",
        )

    with stat3:
        st.metric(
            "Lowest Close",
            f"₹{ticker_df['Close'].min():.2f}",
        )

    with stat4:
        st.metric(
            "Average Close",
            f"₹{ticker_df['Close'].mean():.2f}",
        )

    st.divider()

    # =====================================================
    # Dataset Statistics
    # =====================================================
    st.subheader("Dataset Statistics")

    left, right = st.columns(2)

    with left:

        st.metric(
            "Stocks Covered",
            df["Ticker"].nunique(),
        )

        st.metric(
            "Trading Days",
            df["Date"].nunique(),
        )

        st.metric(
            "Highest Price",
            f"₹{df['Close'].max():.2f}",
        )

    with right:

        st.metric(
            "Dataset Records",
            f"{len(df):,}",
        )

        st.metric(
            "Start Date",
            str(df["Date"].min().date()),
        )

        st.metric(
            "End Date",
            str(df["Date"].max().date()),
        )

    st.divider()

    # =====================================================
    # Historical Dataset
    # =====================================================
    with st.expander(
        "View Complete Historical Dataset",
        expanded=False,
    ):

        st.dataframe(
            ticker_df.sort_values(
                "Date",
                ascending=False,
            ),
            width='stretch',
            hide_index=True,
        )
