# ============================================
# Import Required Libraries
# ============================================

import streamlit as st

# ============================================
# Page Configuration
# ============================================

st.set_page_config(
    page_title="About",
    layout="wide"
)

# ============================================
# Page Title
# ============================================

st.title("About This Project")

st.caption("Nifty500 Stock Market Analysis & Prediction Dashboard")

st.divider()

# ============================================
# Project Overview
# ============================================

st.header("Project Overview")

st.write("""
The **Nifty500 Stock Market Analysis & Prediction Dashboard** is an interactive
web application developed using **Streamlit** that enables users to analyze,
visualize, compare, and predict stock prices of companies listed in the
**Nifty 500 Index**.

This project demonstrates a complete **Data Science workflow**, including:

- Data Collection & Cleaning
- Exploratory Data Analysis (EDA)
- Interactive Data Visualization
- Machine Learning Model Development
- Model Deployment using Streamlit

The dashboard provides investors, students, and analysts with valuable insights
into historical stock market performance through interactive charts and
machine learning-based predictions.
""")

st.divider()

# ============================================
# Dataset Information
# ============================================

st.header("Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Dataset Source")

    st.markdown("""
- **Source:** Kaggle
- **Market:** Nifty 500 Companies
- **Data Type:** Historical Stock Prices
- **Frequency:** Daily
""")

with col2:
    st.subheader("Available Features")

    st.markdown("""
- Date
- Ticker
- Open
- High
- Low
- Close
- Volume
- SMA20
- SMA50
- Daily Return
- EMA20
- Lag Features
- Volatility
""")

st.info(
    "The dashboard uses cleaned historical stock market data for analysis "
    "and a feature-engineered dataset for machine learning predictions."
)

st.divider()

# ============================================
# Dashboard Features
# ============================================

st.header("Dashboard Features")

feature1, feature2 = st.columns(2)

with feature1:

    st.success("""
### Dashboard
- Market Overview
- Key Performance Indicators
- Market Summary
- Interactive Charts
""")

    st.success("""
### Stock Analysis
- Company-wise Analysis
- Candlestick Chart
- Closing Price Trend
- Volume Analysis
- Statistical Summary
""")

with feature2:

    st.success("""
### Prediction
- Random Forest Prediction
- Next Trading Day Forecast
- Predicted vs Latest Price
""")

    st.success("""
### Stock Comparison
- Compare Two Stocks
- Closing Price Comparison
- Volume Comparison
- Statistical Comparison
""")

st.divider()

# ============================================
# Machine Learning Model
# ============================================

st.header("Machine Learning Model")

st.write("""
The stock price prediction module uses a **Random Forest Regressor**
trained on historical market data.

The model predicts the **next trading day's closing price** using
the latest available market information.
""")

st.subheader("Input Features")

st.code("""
Open
High
Low
Volume
SMA20
SMA50
""")

st.subheader("Prediction Workflow")

st.markdown("""
1. Select a stock.
2. Retrieve the latest available market data.
3. Extract required features.
4. Load the trained Random Forest model.
5. Predict the next trading day's closing price.
6. Display prediction and price difference.
""")

st.divider()

# ============================================
# Model Performance
# ============================================

st.header("Model Performance")

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "MAE",
    "30.79"
)

metric2.metric(
    "RMSE",
    "136.72"
)

metric3.metric(
    "R² Score",
    "0.9996"
)

st.info(
    "These metrics were obtained using the historical dataset during model evaluation."
)

st.divider()

# ============================================
# Technologies Used
# ============================================

st.header("Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.markdown("""
### Programming

- Python
- Pandas
- NumPy
""")

with tech2:
    st.markdown("""
### Visualization

- Streamlit
- Plotly
""")

with tech3:
    st.markdown("""
### Machine Learning

- Scikit-learn
- Joblib
""")

st.divider()

# ============================================
# Future Improvements
# ============================================

st.header("Future Improvements")

st.markdown("""
- Live Stock Market Data Integration
- Time-Series Forecasting Models (LSTM, XGBoost)
- NSE Holiday Calendar Support
- Technical Indicator Dashboard
- Portfolio Management
- Risk Analysis
- Investment Recommendation System
- News Sentiment Analysis
- Model Retraining with Latest Data
""")

st.divider()

# ============================================
# Developer Information
# ============================================

st.header("Developer")

st.write("""
**Project:** Nifty500 Stock Market Analysis & Prediction Dashboard

**Developed By:** Vardhan Shah

**Purpose:** Data Science Internship Project

**Framework:** Streamlit

**Machine Learning Model:** Random Forest Regressor
""")

st.success("Thank you for exploring the Nifty500 Stock Market Dashboard!")