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
    # Prepare Model Input
    # -----------------------
    X = pd.DataFrame(
        [[
            latest["Open"],
            latest["High"],
            latest["Low"],
            latest["Volume"],
            latest["SMA20"],
            latest["SMA50"],
        ]],
        columns=[
            "Open",
            "High",
            "Low",
            "Volume",
            "SMA20",
            "SMA50",
        ]
    )

    # -----------------------
    # Predict Next Close Price
    # -----------------------
    prediction = model.predict(X)[0]

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
            delta=f"₹{prediction - latest['Close']:.2f}"
        )

    # -----------------------
    # Model Performance
    # -----------------------
    st.subheader("Model Information")

    st.write("Model : Random Forest Regressor")
    st.write("Training Split : 80%")
    st.write("Testing Split : 20%")
    st.write("Features Used : Open, High, Low, Volume, SMA20, SMA50")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("MAE", "30.79")

    with col2:
        st.metric("RMSE", "136.72")

    with col3:
        st.metric("R² Score", "0.9996")
