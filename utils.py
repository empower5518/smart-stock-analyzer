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
