import streamlit as st

st.set_page_config(
    page_title="Nifty500 Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("Nifty500 Stock Market Dashboard")

st.markdown("""
## Welcome

This project analyzes Nifty500 stocks using Machine Learning.

Use the navigation panel on the left to explore:

- Dashboard
- Stock Analysis
- Price Prediction
- Model Performance
- About
""")