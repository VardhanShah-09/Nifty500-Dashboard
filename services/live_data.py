"""
Live Market Data Service
------------------------
Fetches live NSE stock data using Yahoo Finance.
"""
import streamlit as st
from datetime import datetime
import yfinance as yf
import pandas as pd

@st.cache_data(ttl=30, show_spinner=False)
def get_live_stock_data(symbol: str):
    """
    Fetch live stock information from Yahoo Finance.

    Parameters
    ----------
    symbol : str
        NSE ticker without '.NS'
        Example:
            RELIANCE
            TCS
            INFY

    Returns
    -------
    dict
        Live market information.
    """

    try:

        ticker = yf.Ticker(f"{symbol.upper()}.NS")

        info = ticker.fast_info

        return {
            "success": True,
            "ticker": f"{symbol.upper()}.NS",
            "price": info.get("lastPrice"),
            "open": info.get("open"),
            "high": info.get("dayHigh"),
            "low": info.get("dayLow"),
            "previous_close": info.get("previousClose"),
            "volume": info.get("lastVolume"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange"),
            "last_updated": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
        }

@st.cache_data(ttl=300, show_spinner=False)
def get_historical_stock_data(symbol: str, period: str = "5y"):
    """
    Fetch historical OHLCV data from Yahoo Finance.

    Parameters
    ----------
    symbol : str
        NSE ticker without '.NS'
        Example:
            RELIANCE
            TCS
            INFY

    period : str
        Supported values:
        1mo, 3mo, 6mo, 1y, 2y, 5y, max

    Returns
    -------
    pandas.DataFrame
        Columns:
        Date
        Open
        High
        Low
        Close
        Volume
    """

    try:

        ticker = yf.Ticker(f"{symbol.upper()}.NS")

        df = ticker.history(
            period=period,
            auto_adjust=False
        )

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()

        df = df[
            [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
            ]
        ]

        df["Date"] = pd.to_datetime(df["Date"])
        
        # =====================================================
        # Technical Indicators
        # =====================================================

        # Simple Moving Averages
        df["SMA20"] = df["Close"].rolling(20).mean()
        df["SMA50"] = df["Close"].rolling(50).mean()

        # Relative Strength Index
        df["RSI"] = calculate_rsi(df["Close"])

        # MACD
        (
            df["EMA12"],
            df["EMA26"],
            df["MACD"],
            df["Signal"],
            df["Histogram"],
        ) = calculate_macd(df["Close"])
        
        # Bollinger Bands
        (
            df["Upper_Band"],
            _,
            df["Lower_Band"],
        ) = calculate_bollinger_bands(df["Close"])

        return df

    except Exception as e:

        print(f"Historical Data Error: {e}")

        return pd.DataFrame()

# =====================================================
# RSI Indicator
# =====================================================

def calculate_rsi(close_prices, period=14):
    """
    Calculate Relative Strength Index (RSI).
    Returns a Pandas Series.
    """

    delta = close_prices.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


# =====================================================
# Exponential Moving Average (EMA)
# =====================================================

def calculate_ema(close_prices, period):
    """
    Calculate Exponential Moving Average (EMA).
    Returns a Pandas Series.
    """

    return close_prices.ewm(span=period, adjust=False).mean()


# =====================================================
# MACD Indicator
# =====================================================

def calculate_macd(close_prices):
    """
    Calculate MACD, Signal Line and Histogram.
    Returns three Pandas Series.
    """

    ema12 = calculate_ema(close_prices, 12)
    ema26 = calculate_ema(close_prices, 26)

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    return ema12, ema26, macd, signal, histogram
    

# =====================================================
# Bollinger Bands
# =====================================================

def calculate_bollinger_bands(close_prices, period=20, std_dev=2):
    """
    Calculate Bollinger Bands.
    Returns Upper Band, Middle Band (SMA), and Lower Band.
    """

    middle_band = close_prices.rolling(window=period).mean()

    rolling_std = close_prices.rolling(window=period).std()

    upper_band = middle_band + (rolling_std * std_dev)
    lower_band = middle_band - (rolling_std * std_dev)

    return upper_band, middle_band, lower_band


@st.cache_data(ttl=300, show_spinner=False)
def prepare_prediction_features(symbol: str):
    """
    Prepare the latest feature vector for the prediction model.

    Features returned:
        Open
        High
        Low
        Volume
        SMA20
        SMA50
        Close
        Date
    """

    try:

        # Download 5 years of history
        df = get_historical_stock_data(
            symbol,
            period="5y"
        )

        if df.empty:
            return None

        # -----------------------
        # Feature Engineering
        # -----------------------

        df["SMA20"] = (
            df["Close"]
            .rolling(window=20)
            .mean()
        )

        df["SMA50"] = (
            df["Close"]
            .rolling(window=50)
            .mean()
        )
        
        df["RSI"] = calculate_rsi(df["Close"])

        # Remove rows where moving averages
        # cannot yet be calculated
        df = df.dropna().reset_index(drop=True)

        if df.empty:
            return None

        latest = df.iloc[-1]

        latest_data = {
            "Date": latest["Date"],

            "Open": latest["Open"],
            "High": latest["High"],
            "Low": latest["Low"],
            "Close": latest["Close"],
            "Volume": latest["Volume"],

            # Moving Averages
            "SMA20": latest["SMA20"],
            "SMA50": latest["SMA50"],
            "EMA12": latest["EMA12"],
            "EMA26": latest["EMA26"],

            # Momentum
            "RSI": latest["RSI"],

            # MACD
            "MACD": latest["MACD"],
            "Signal": latest["Signal"],
            "Histogram": latest["Histogram"],

            # Bollinger Bands
            "Upper_Band": latest["Upper_Band"],
            "Lower_Band": latest["Lower_Band"],
        }
        
        return latest_data, df

    except Exception as e:

        print(f"Prediction Feature Error: {e}")

        return None
