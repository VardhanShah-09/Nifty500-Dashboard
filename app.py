import streamlit as st

from components.Dashboard import show as dashboard
from components.Stock_Analysis import show as stock_analysis
from components.Prediction import show as prediction
from components.Comparison import show as comparison
from components.About import show as about

st.set_page_config(
    page_title="Nifty500 Dashboard",
    page_icon="📈",
    layout="wide"
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "📈 Stock Analysis",
    "🤖 Prediction",
    "⚖️ Comparison",
    "ℹ️ About"
])

with tab1:
    dashboard()

with tab2:
    stock_analysis()

with tab3:
    prediction()

with tab4:
    comparison()

with tab5:
    about()

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
