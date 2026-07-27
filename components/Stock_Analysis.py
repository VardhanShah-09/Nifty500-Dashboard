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
    # Page Configuration
    # =====================================================
    st.set_page_config(
        page_title="Stock Analysis",
        layout="wide"
    )

    # =====================================================
    # Load Ticker List
    # =====================================================
    df = load_data()

    # =====================================================
    # Sidebar
    # =====================================================
    st.sidebar.title("📈 Stock Analysis")

    ticker = st.sidebar.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="analysis_stock"
    )

    period = st.sidebar.selectbox(
        "Select Time Period",
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
        key="analysis_period"
    )

    # =====================================================
    # Load Historical Data
    # =====================================================
    with st.spinner("Loading historical market data..."):

        stock_df = get_historical_stock_data(
            ticker,
            period
        )

    if stock_df.empty:
        st.error("Unable to fetch stock data.")
        st.stop()

    stock_df = stock_df.sort_values("Date")

    latest = stock_df.iloc[-1]

    # =====================================================
    # Header
    # =====================================================
    st.title("📈 Stock Analysis")

    st.caption(
        f"Technical analysis for **{ticker}** "
        f"over the selected period."
    )

    # =====================================================
    # Live Metrics
    # =====================================================
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Current Price",
            f"₹{latest['Close']:.2f}"
        )

    with col2:
        st.metric(
            "52 Period High",
            f"₹{stock_df['High'].max():.2f}"
        )

    with col3:
        st.metric(
            "52 Period Low",
            f"₹{stock_df['Low'].min():.2f}"
        )

    with col4:
        st.metric(
            "Average Volume",
            f"{stock_df['Volume'].mean():,.0f}"
        )

    with col5:

        change = latest["Close"] - stock_df.iloc[-2]["Close"]

        st.metric(
            "Daily Change",
            f"₹{change:.2f}",
            f"{change:.2f}"
        )

    st.divider()

    # =====================================================
    # Candlestick + Technical Indicators
    # =====================================================
    st.subheader("Candlestick Chart")

    fig = go.Figure()

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=stock_df["Date"],
            open=stock_df["Open"],
            high=stock_df["High"],
            low=stock_df["Low"],
            close=stock_df["Close"],
            name="Price"
        )
    )

    # SMA20
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["SMA20"],
            mode="lines",
            name="SMA20",
            line=dict(width=2)
        )
    )

    # SMA50
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["SMA50"],
            mode="lines",
            name="SMA50",
            line=dict(width=2)
        )
    )

    # Upper Bollinger Band
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Upper_Band"],
            mode="lines",
            name="Upper Band",
            line=dict(
                dash="dot",
                width=1.5
            )
        )
    )

    # Lower Bollinger Band
    fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Lower_Band"],
            mode="lines",
            name="Lower Band",
            line=dict(
                dash="dot",
                width=1.5
            )
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        title=f"{ticker} Price Action",
        xaxis_rangeslider_visible=False,
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

    # =====================================================
    # Volume Chart
    # =====================================================
    st.subheader("Trading Volume")

    volume_fig = px.bar(
        stock_df,
        x="Date",
        y="Volume",
        title="Daily Trading Volume"
    )

    volume_fig.update_layout(
        template="plotly_dark",
        height=350,
        showlegend=False
    )

    st.plotly_chart(
        volume_fig,
        width="stretch"
    )
    
        # =====================================================
    # RSI Chart
    # =====================================================
    st.subheader("Relative Strength Index (RSI)")

    rsi_fig = go.Figure()

    rsi_fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["RSI"],
            mode="lines",
            name="RSI",
            line=dict(width=2)
        )
    )

    rsi_fig.add_hline(
        y=70,
        line_dash="dash",
        annotation_text="Overbought (70)"
    )

    rsi_fig.add_hline(
        y=30,
        line_dash="dash",
        annotation_text="Oversold (30)"
    )

    rsi_fig.add_hline(
        y=50,
        line_dash="dot"
    )

    rsi_fig.update_layout(
        template="plotly_dark",
        height=350,
        yaxis=dict(range=[0, 100]),
        showlegend=False,
    )

    st.plotly_chart(
        rsi_fig,
        width="stretch"
    )

    # =====================================================
    # MACD Chart
    # =====================================================
    st.subheader("MACD")

    macd_fig = go.Figure()

    macd_fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["MACD"],
            mode="lines",
            name="MACD"
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=stock_df["Date"],
            y=stock_df["Signal"],
            mode="lines",
            name="Signal"
        )
    )

    macd_fig.add_trace(
        go.Bar(
            x=stock_df["Date"],
            y=stock_df["Histogram"],
            name="Histogram"
        )
    )

    macd_fig.update_layout(
        template="plotly_dark",
        height=400,
        barmode="relative"
    )

    st.plotly_chart(
        macd_fig,
        width="stretch"
    )

    # =====================================================
    # Technical Summary
    # =====================================================
    st.subheader("Technical Summary")

    latest = stock_df.iloc[-1]

    trend = "Sideways"
    trend_color = "🟡"

    if latest["Close"] > latest["SMA20"] > latest["SMA50"]:
        trend = "Bullish"
        trend_color = "🟢"

    elif latest["Close"] < latest["SMA20"] < latest["SMA50"]:
        trend = "Bearish"
        trend_color = "🔴"

    if latest["RSI"] > 70:
        rsi_status = "Overbought"
        rsi_icon = "🔴"

    elif latest["RSI"] < 30:
        rsi_status = "Oversold"
        rsi_icon = "🟢"

    else:
        rsi_status = "Neutral"
        rsi_icon = "🟡"

    if latest["MACD"] > latest["Signal"]:
        macd_status = "Bullish Crossover"
        macd_icon = "🟢"

    else:
        macd_status = "Bearish Crossover"
        macd_icon = "🔴"

    col1, col2 = st.columns(2)

    with col1:

        st.success("Market Trend")

        st.write(f"**Trend :** {trend_color} {trend}")

        st.write(
            f"**Price :** ₹{latest['Close']:.2f}"
        )

        st.write(
            f"**SMA20 :** ₹{latest['SMA20']:.2f}"
        )

        st.write(
            f"**SMA50 :** ₹{latest['SMA50']:.2f}"
        )

    with col2:

        st.info("Momentum Indicators")

        st.write(
            f"**RSI :** {rsi_icon} {latest['RSI']:.2f} ({rsi_status})"
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

        st.write(
            f"**MACD Signal :** {macd_icon} {macd_status}"
        )

    # =====================================================
    # Statistics
    # =====================================================
    st.subheader("Statistics")

    stat1, stat2 = st.columns(2)

    with stat1:

        st.write(
            f"Highest Close : ₹{stock_df['Close'].max():.2f}"
        )

        st.write(
            f"Lowest Close : ₹{stock_df['Close'].min():.2f}"
        )

        st.write(
            f"Average Close : ₹{stock_df['Close'].mean():.2f}"
        )

        st.write(
            f"Standard Deviation : ₹{stock_df['Close'].std():.2f}"
        )

    with stat2:

        st.write(
            f"Trading Days : {len(stock_df)}"
        )

        st.write(
            f"Average Volume : {stock_df['Volume'].mean():,.0f}"
        )

        st.write(
            f"Maximum Volume : {stock_df['Volume'].max():,.0f}"
        )

        st.write(
            f"Minimum Volume : {stock_df['Volume'].min():,.0f}"
        )

    # =====================================================
    # Historical Data
    # =====================================================
    with st.expander("View Historical Data", expanded=False):

        st.dataframe(
            stock_df,
            width="stretch",
            hide_index=True
        )
