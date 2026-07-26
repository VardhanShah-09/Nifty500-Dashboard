"""
Live Market Data Service
------------------------
Fetches live NSE stock data using Yahoo Finance.
"""

from datetime import datetime
import yfinance as yf
import pandas as pd

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

        return df

    except Exception as e:

        print(f"Historical Data Error: {e}")

        return pd.DataFrame()
    
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

        # Remove rows where moving averages
        # cannot yet be calculated
        df = df.dropna().reset_index(drop=True)

        if df.empty:
            return None

        latest = df.iloc[-1]

        return {
            "Date": latest["Date"],
            "Open": latest["Open"],
            "High": latest["High"],
            "Low": latest["Low"],
            "Close": latest["Close"],
            "Volume": latest["Volume"],
            "SMA20": latest["SMA20"],
            "SMA50": latest["SMA50"],
        }

    except Exception as e:

        print(f"Prediction Feature Error: {e}")

        return None
