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

    # =====================================================
    # Load Dataset
    # =====================================================
    df = load_data()

    # =====================================================
    # Page Header
    # =====================================================
    st.title("Stock Analysis")
    st.caption(
        "Analyze historical price movements and technical indicators for any Nifty500 stock."
    )

    st.divider()

    # =====================================================
    # Stock Selection
    # =====================================================
    col1, col2 = st.columns(2)

    with col1:

        ticker = st.selectbox(
            "Select Stock",
            sorted(df["Ticker"].unique()),
            key="analysis_stock",
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
            key="analysis_period",
        )

    st.divider()

    # =====================================================
    # Load Historical Data
    # =====================================================
    with st.spinner("Loading market data..."):

        stock_df = get_historical_stock_data(
            ticker,
            period,
        )

    if stock_df.empty:
        st.error("Unable to fetch stock data.")
        st.stop()

    stock_df = stock_df.sort_values("Date")

    latest = stock_df.iloc[-1]

    # =====================================================
    # Overview
    # =====================================================
    st.subheader("Market Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    previous_close = stock_df.iloc[-2]["Close"]

    daily_change = latest["Close"] - previous_close

    daily_change_pct = (
        daily_change / previous_close
    ) * 100

    with col1:

        st.metric(
            "Current Price",
            f"₹{latest['Close']:.2f}",
            f"{daily_change:+.2f}",
        )

    with col2:

        st.metric(
            "Period High",
            f"₹{stock_df['High'].max():.2f}",
        )

    with col3:

        st.metric(
            "Period Low",
            f"₹{stock_df['Low'].min():.2f}",
        )

    with col4:

        st.metric(
            "Average Volume",
            f"{stock_df['Volume'].mean():,.0f}",
        )

    with col5:

        st.metric(
            "Daily Return",
            f"{daily_change_pct:+.2f}%",
        )

    st.divider()

    # =====================================================
    # Technical Snapshot
    # =====================================================
    st.subheader("📈 Technical Snapshot")

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

    if latest["MACD"] > latest["Signal"]:
        macd_status = "Bullish"

    else:
        macd_status = "Bearish"

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
            rsi_status,
        )

    with c3:

        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}",
            macd_status,
        )

    with c4:

        st.metric(
            "SMA20",
            f"₹{latest['SMA20']:.2f}",
        )

    st.divider()

    # =====================================================
    # Price Action
    # =====================================================
    st.subheader("Price Action")

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"],
            name="Price",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["SMA20"],
            mode="lines",
            name="SMA20",
            line=dict(width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["SMA50"],
            mode="lines",
            name="SMA50",
            line=dict(width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Upper_Band"],
            mode="lines",
            name="Upper Band",
            line=dict(width=1, dash="dot"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Lower_Band"],
            mode="lines",
            name="Lower Band",
            line=dict(width=1, dash="dot"),
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        title=f"{ticker} Price Chart",
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
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
    # Volume Analysis
    # =====================================================
    st.subheader("Volume Analysis")

    volume_fig = px.bar(
        stock_df,
        x="Date",
        y="Volume",
        title="Trading Volume",
    )

    volume_fig.update_layout(
        template="plotly_dark",
        height=350,
        showlegend=False,
    )

    st.plotly_chart(
        volume_fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # RSI Analysis
    # =====================================================
    st.subheader("Relative Strength Index")

    rsi_fig = go.Figure()

    rsi_fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["RSI"],
            mode="lines",
            name="RSI",
        )
    )

    rsi_fig.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Overbought",
    )

    rsi_fig.add_hline(
        y=30,
        line_dash="dash",
        annotation_text="Oversold",
    )

    rsi_fig.update_layout(
        template="plotly_dark",
        height=350,
        yaxis=dict(range=[0, 100]),
        showlegend=False,
    )

    st.plotly_chart(
        rsi_fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # MACD Analysis
    # =====================================================
    st.subheader("MACD")

    macd_fig = go.Figure()

    macd_fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["MACD"],
            name="MACD",
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Signal"],
            name="Signal",
        )
    )

    macd_fig.add_trace(
        go.Bar(
            x=stock_df["Date"],
            y=stock_df["Histogram"],
            name="Histogram",
        )
    )

    macd_fig.update_layout(
        template="plotly_dark",
        height=400,
        barmode="relative",
    )

    st.plotly_chart(
        macd_fig,
        width="stretch",
    )

    st.divider()

    # =====================================================
    # Performance Statistics
    # =====================================================
    st.subheader("Performance Statistics")

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:

        st.metric(
            "Highest Close",
            f"₹{stock_df['Close'].max():.2f}",
        )

    with stat2:

        st.metric(
            "Lowest Close",
            f"₹{stock_df['Close'].min():.2f}",
        )

    with stat3:

        st.metric(
            "Average Close",
            f"₹{stock_df['Close'].mean():.2f}",
        )

    with stat4:

        st.metric(
            "Trading Days",
            len(stock_df),
        )

    st.divider()

    # =====================================================
    # Volume Statistics
    # =====================================================
    st.subheader("Volume Statistics")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Average Volume",
            f"{stock_df['Volume'].mean():,.0f}",
        )

    with c2:

        st.metric(
            "Maximum Volume",
            f"{stock_df['Volume'].max():,.0f}",
        )

    with c3:

        st.metric(
            "Minimum Volume",
            f"{stock_df['Volume'].min():,.0f}",
        )

    st.divider()

    # =====================================================
    # Historical Dataset
    # =====================================================
    with st.expander(
        "View Historical Market Data",
        expanded=False,
    ):

        st.dataframe(
            stock_df.sort_values(
                "Date",
                ascending=False,
            ),
            width="stretch",
            hide_index=True,
        )

    st.divider()

    st.caption(
        "Historical market data sourced from Yahoo Finance. "
        "Technical indicators are calculated using historical OHLCV data."
    )
