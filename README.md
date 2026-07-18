# Nifty500 Stock Market Analysis & Prediction Dashboard

An interactive **Stock Market Analytics Dashboard** built with **Streamlit** that enables users to explore, analyze, compare, and predict stock prices of companies listed in the **Nifty 500 Index**.

This project was developed as part of a **Data Science Internship Project** and demonstrates an end-to-end data science workflow, including data preprocessing, visualization, machine learning, and web application deployment.

---

# Features

### Market Dashboard
- Market Overview
- Total Stocks
- Total Records
- Average Closing Price
- Average Trading Volume
- Recent Market Data

---

### Stock Analysis
- Company-wise Analysis
- Interactive Closing Price Chart
- Candlestick Chart
- Volume Analysis
- Statistical Summary

---

### Stock Price Prediction
- Random Forest Regressor
- Predicts Next Trading Day Closing Price
- Uses Latest Market Data
- Displays Prediction Difference

---

### Stock Comparison
- Compare Two Companies
- Closing Price Comparison
- Volume Comparison
- Statistical Comparison
- Historical Data Tables

---

### About Page
- Project Overview
- Dataset Information
- Machine Learning Details
- Technologies Used
- Future Scope

---

# Dataset

The datasets are not included in this repository because of GitHub's file size limits.

You can download them from:

https://www.kaggle.com/datasets/shreyashautomation/nifty500-companies-5-years-stock-market-data

After downloading, place them in:

Data/
    Raw_data/
    Processed_data/

**Source:** Kaggle

**Dataset:** Nifty 500 Companies – 5 Years Stock Market Data

The project uses:

- Historical Stock Prices
- Open
- High
- Low
- Close
- Volume

A feature-engineered dataset is also used for machine learning, including:

- SMA20
- SMA50
- EMA20
- Daily Return
- Lag Features
- Volatility

---

# Machine Learning Model

Model Used:

- Random Forest Regressor

Input Features:

- Open
- High
- Low
- Volume
- SMA20
- SMA50

Prediction Target:

- Next Trading Day Closing Price

---

# Model Performance

| Metric | Score |
|---------|-------|
| MAE | 30.79 |
| RMSE | 136.72 |
| R² Score | 0.9996 |

> **Note:** These metrics were obtained using the historical dataset during model evaluation. The project is intended as an educational demonstration. A production-grade forecasting system would use time-series validation and live market data.

---

# Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Joblib

---

# Project Structure

```text
Nifty500/
│
├── app.py
├── models/
│   └── random_forest.pkl
│
├── utils/
│   └── loader.py
│
├── Data/
│   └── Processed_data/
│       ├── cleaned_nifty500.csv
│       └── features_nifty500.csv
│
├── pages/
│   ├── Dashboard.py
│   ├── Stock_Analysis.py
│   ├── Prediction.py
│   ├── Comparison.py
│   └── About.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project folder

```bash
cd Nifty500
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# Screenshots

## Dashboard

> *(Add screenshot here)*

---

## Stock Analysis

> *(Add screenshot here)*

---

## Prediction

> *(Add screenshot here)*

---

## Stock Comparison

> *(Add screenshot here)*

---

## About

> *(Add screenshot here)*

---

# Future Improvements

- Live Market Data Integration
- Time-Series Forecasting
- LSTM/XGBoost Models
- NSE Holiday Calendar
- Portfolio Analysis
- Technical Indicators
- Investment Recommendation System
- News Sentiment Analysis
- Automatic Model Retraining

---

# Developer

**Vardhan Shah**

Data Science Internship Project

---

⭐ If you found this project useful, consider giving it a star.