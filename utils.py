import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

def plot_stock_chart(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        hist = ticker.history(period="6mo")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(hist.index, hist['Close'], label='Close Price', color='blue')
        ax.set_title(f"{symbol} - Price Trend (6 months)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (₹)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"Could not load chart for {symbol}: {e}")

def is_bouncing_from_bottom(hist):
    try:
        lowest = hist['Close'].min()
        highest = hist['Close'].max()
        recent = hist['Close'].iloc[-1]
        downtrend = lowest < 0.75 * highest
        recovering = recent > lowest * 1.2
        return downtrend and recovering
    except:
        return False

def has_volume_spike(hist):
    try:
        weekly_vol = hist['Volume'].resample('W').sum()
        if len(weekly_vol) < 2:
            return False
        latest_vol = weekly_vol.iloc[-1]
        avg_vol = weekly_vol[:-1].mean()
        return (latest_vol > 3 * avg_vol) or (latest_vol > 1_000_000)
    except:
        return False
