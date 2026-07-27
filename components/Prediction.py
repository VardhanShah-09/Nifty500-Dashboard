import streamlit as st
import pandas as pd
from utils.loader import load_data, load_model
from services.live_data import prepare_prediction_features

def show():
    # -----------------------
    # Page Configuration
    # -----------------------
    st.set_page_config(
        page_title="Prediction",
        layout="wide"
    )

    # -----------------------
    # Load Dataset
    # -----------------------
    df = load_data()
    model = load_model()
    
    # -----------------------
    # Sidebar
    # -----------------------
    st.sidebar.title("Prediction")

    ticker = st.sidebar.selectbox(
        "Select Stock",
        sorted(df["Ticker"].unique()),
        key="prediction_stock"
    )

    # -----------------------
    # Selected Stock Data
    # -----------------------
    latest = prepare_prediction_features(ticker)

    if latest is None:
        st.warning("No prediction data available.")
        st.stop()
    # -----------------------
    # Header
    # -----------------------
    st.title("Stock Price Prediction")

    st.caption("Predict the next closing price using the trained Random Forest model.")

    # -----------------------
    # Latest Stock Values
    # -----------------------
    st.subheader("Latest Market Values")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Open", f"₹{latest['Open']:.2f}")

    with col2:
        st.metric("High", f"₹{latest['High']:.2f}")

    with col3:
        st.metric("Low", f"₹{latest['Low']:.2f}")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Volume", f"{latest['Volume']:,.0f}")

    with col5:
        st.metric("SMA20", f"₹{latest['SMA20']:.2f}")

    with col6:
        st.metric("SMA50", f"₹{latest['SMA50']:.2f}")
    
    # -----------------------
    # Technical Indicators
    # -----------------------

    st.subheader("Technical Indicators")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "RSI",
            f"{latest['RSI']:.2f}"
        )

    with c2:
        st.metric(
            "MACD",
            f"{latest['MACD']:.2f}"
        )

    with c3:
        st.metric(
            "Signal",
            f"{latest['Signal']:.2f}"
        )

    with c4:
        st.metric(
            "Histogram",
            f"{latest['Histogram']:.2f}"
        )

    c5, c6 = st.columns(2)

    with c5:
        st.metric(
            "Upper Band",
            f"₹{latest['Upper_Band']:.2f}"
        )

    with c6:
        st.metric(
            "Lower Band",
            f"₹{latest['Lower_Band']:.2f}"
        )

    st.divider()
        
    # -----------------------
    # Prepare Model Input
    # -----------------------
    X = pd.DataFrame([{
        "Open": latest["Open"],
        "High": latest["High"],
        "Low": latest["Low"],
        "Volume": latest["Volume"],

        "SMA20": latest["SMA20"],
        "SMA50": latest["SMA50"],

        "EMA12": latest["EMA12"],
        "EMA26": latest["EMA26"],

        "RSI": latest["RSI"],

        "MACD": latest["MACD"],
        "Signal": latest["Signal"],
        "Histogram": latest["Histogram"],

        "Upper_Band": latest["Upper_Band"],
        "Lower_Band": latest["Lower_Band"],
    }])

    # -----------------------
    # Predict Next Close Price
    # -----------------------
    prediction = model.predict(X)[0]
    
    # -----------------------
    # Prediction Summary
    # -----------------------

    change = prediction - latest["Close"]

    change_pct = (
        change /
        latest["Close"]
    ) * 100

    # -----------------------
    # Prediction Result
    # -----------------------
    st.subheader("Prediction Result")

    prediction_date = latest["Date"] + pd.offsets.BDay(1)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Prediction Date",
            prediction_date.strftime("%d-%m-%Y")
        )

    with col2:
        st.metric(
            "Latest Close",
            f"₹{latest['Close']:.2f}"
        )

    with col3:
        st.metric(
            "Predicted Next Close",
            f"₹{prediction:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)"
        )

    # -----------------------
    # Prediction Direction
    # -----------------------

    if prediction > latest["Close"]:

        st.success(
            "📈 The model predicts an upward movement for the next trading session."
        )

    elif prediction < latest["Close"]:

        st.error("📉 The model predicts a downward movement for the next trading session.")

    else:

        st.info("➖ The model predicts minimal price movement.")

    st.divider()

    # -----------------------
    # Model Performance
    # -----------------------
    st.subheader("Model Information")

    st.write("Model : Random Forest Regressor")
    st.write("Training Split : 80%")
    st.write("Testing Split : 20%")
    st.write("""
        **Features Used**

        • Open
        • High
        • Low
        • Volume
        • SMA20
        • SMA50
        • EMA12
        • EMA26
        • RSI
        • MACD
        • Signal
        • Histogram
        • Upper Bollinger Band
        • Lower Bollinger Band
        """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("MAE", "YOUR_MAE")

    with col2:
        st.metric("RMSE", "YOUR_RMSE")

    with col3:
        st.metric("R² Score", "YOUR_R2")
