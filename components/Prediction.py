import streamlit as st
import pandas as pd

from utils.loader import load_data
from services.live_data import prepare_prediction_features
from services.prediction_model import predict_stock


def show():

    # =====================================================
    # Load Dataset
    # =====================================================
    df = load_data()

    # =====================================================
    # Header
    # =====================================================
    st.title("Stock Price Prediction")
    st.caption(
        "Predict the next trading session closing price using Machine Learning and Deep Learning models."
    )

    st.divider()

    # =====================================================
    # Prediction Configuration
    # =====================================================
    st.subheader("Prediction Configuration")

    col1, col2 = st.columns(2)

    with col1:

        ticker = st.selectbox(
            "Select Stock",
            sorted(df["Ticker"].unique()),
            key="prediction_stock",
        )

    with col2:

        model_name = st.selectbox(
            "Prediction Model",
            [
                "Random Forest",
                "XGBoost",
                "LSTM",
            ],
            key="prediction_model",
        )
        
    st.divider()

    # =====================================================
    # Fetch Prediction Features
    # =====================================================
    result = prepare_prediction_features(ticker)

    if result is None:
        st.warning("No prediction data available.")
        st.stop()

    latest, stock_history = result

    # =====================================================
    # Latest Market Snapshot
    # =====================================================
    st.subheader("Latest Market Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Current Price",
            f"₹{latest['Close']:.2f}",
        )

    with c2:
        st.metric(
            "Open",
            f"₹{latest['Open']:.2f}",
        )

    with c3:
        st.metric(
            "High",
            f"₹{latest['High']:.2f}",
        )

    with c4:
        st.metric(
            "Low",
            f"₹{latest['Low']:.2f}",
        )

    st.write("")

    c5, c6, c7 = st.columns(3)

    with c5:
        st.metric(
            "Volume",
            f"{latest['Volume']:,.0f}",
        )

    with c6:
        st.metric(
            "SMA20",
            f"₹{latest['SMA20']:.2f}",
        )

    with c7:
        st.metric(
            "SMA50",
            f"₹{latest['SMA50']:.2f}",
        )

    st.divider()

    # =====================================================
    # Technical Indicators
    # =====================================================
    st.subheader("Technical Indicators")

    row1 = st.columns(4)

    with row1[0]:
        st.metric(
            "RSI",
            f"{latest['RSI']:.2f}",
        )

    with row1[1]:
        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}",
        )

    with row1[2]:
        st.metric(
            "Signal",
            f"{latest['Signal']:.2f}",
        )

    with row1[3]:
        st.metric(
            "Histogram",
            f"{latest['Histogram']:.2f}",
        )

    st.write("")

    row2 = st.columns(2)

    with row2[0]:
        st.metric(
            "Upper Bollinger Band",
            f"₹{latest['Upper_Band']:.2f}",
        )

    with row2[1]:
        st.metric(
            "Lower Bollinger Band",
            f"₹{latest['Lower_Band']:.2f}",
        )

    st.divider()

    # =====================================================
    # Predict Next Close Price
    # =====================================================

    if model_name == "LSTM":

        prediction = predict_stock(
            model_name=model_name,
            latest=latest,
            history=stock_history,
        )

    else:

        prediction = predict_stock(
            model_name=model_name,
            latest=latest,
        )

    # =====================================================
    # Prediction Summary
    # =====================================================

    change = prediction - latest["Close"]
    change_pct = (change / latest["Close"]) * 100

    prediction_date = latest["Date"] + pd.offsets.BDay(1)

    # =====================================================
    # Prediction Result
    # =====================================================
    st.subheader("Prediction Result")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Prediction Date",
            prediction_date.strftime("%d %b %Y"),
        )

    with col2:

        st.metric(
            "Current Close",
            f"₹{latest['Close']:.2f}",
        )

    with col3:

        st.metric(
            "Predicted Close",
            f"₹{prediction:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)",
        )

    st.write("")

    if prediction > latest["Close"]:

        st.success(
            "📈 **Bullish Outlook**\n\nThe selected model predicts an upward movement for the next trading session."
        )

    elif prediction < latest["Close"]:

        st.error(
            "📉 **Bearish Outlook**\n\nThe selected model predicts a downward movement for the next trading session."
        )

    else:

        st.info(
            "➖ **Neutral Outlook**\n\nThe selected model predicts minimal price movement."
        )

    st.divider()

    # =====================================================
    # Model Information
    # =====================================================
    st.subheader("Model Information")

    left, right = st.columns([2, 2])

    with left:

        st.markdown(f"**Selected Model:** `{model_name}`")

        st.markdown("**Training Split:** 80%")

        st.markdown("**Testing Split:** 20%")

    with right:

        st.metric(
            "Prediction",
            f"₹{prediction:.2f}",
        )

        st.metric(
            "Expected Return",
            f"{change_pct:+.2f}%",
        )

        st.metric(
            "Direction",
            "Bullish" if change > 0 else "Bearish",
        )

    st.divider()

    # =====================================================
    # Prediction Summary
    # =====================================================

    with st.expander(
        "Prediction Summary",
        expanded=False,
    ):

        summary = pd.DataFrame(
            {
                "Parameter": [
                    "Stock",
                    "Model",
                    "Prediction Date",
                    "Current Close",
                    "Predicted Close",
                    "Expected Change",
                    "Expected Return",
                ],
                "Value": [
                    ticker,
                    model_name,
                    prediction_date.strftime("%d-%m-%Y"),
                    f"₹{latest['Close']:.2f}",
                    f"₹{prediction:.2f}",
                    f"{change:+.2f}",
                    f"{change_pct:+.2f}%",
                ],
            }
        )

        st.dataframe(
            summary,
            width='stretch',
            hide_index=True,
        )

    st.divider()

    st.caption(
        "Prediction generated using the selected Machine Learning model. "
        "Live market data is sourced from Yahoo Finance. "
        "This prediction is for educational purposes only and should not be considered financial advice."
    )
