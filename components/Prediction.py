import streamlit as st
import pandas as pd
from utils.loader import load_features, load_model

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
    df = load_features()
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
    stock_df = (
        df[df["Ticker"] == ticker]
        .sort_values("Date")
    )

    if stock_df.empty:
        st.warning("No data available for the selected stock.")
        st.stop()

    latest = stock_df.iloc[-1]
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
    features = latest[
        [
            "Open",
            "High",
            "Low",
            "Volume",
            "SMA20",
            "SMA50"
        ]
    ]

    X = pd.DataFrame([features])

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
