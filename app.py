# smart_stock_analyzer/app.py

import streamlit as st
import pandas as pd
from filters import apply_all_filters
from utils import plot_stock_chart

st.set_page_config(page_title="📊 Smart Stock Analyzer", layout="wide")
st.title("📊 Smart Stock Analyzer (NSE Screener)")

with st.sidebar:
    st.header("Filter Settings")
    price_range = st.slider("Price Range (₹)", 150, 800, (150, 800))
    min_roe = st.slider("Minimum ROE (%)", 10, 30, 15)
    max_de_ratio = st.slider("Max Debt-Equity Ratio", 0.0, 1.0, 0.5)
    rsi_threshold = st.slider("Min RSI", 40, 80, 60)
    beta_threshold = st.slider("Max Beta", 0.5, 2.0, 1.2)
    market_caps = st.multiselect("Market Cap Categories", ["Smallcap", "Midcap", "Largecap"], ["Smallcap", "Midcap", "Largecap"])
    sector_filter = st.text_input("Sector (optional):")

if st.button("🔍 Run Screener"):
    with st.spinner("Fetching and filtering stocks..."):
        result_df = apply_all_filters(
            price_range, min_roe, max_de_ratio,
            rsi_threshold, beta_threshold,
            market_caps, sector_filter
        )
        st.success(f"Found {len(result_df)} matching stocks")

        if not result_df.empty:
            st.dataframe(result_df)

            for i, row in result_df.iterrows():
                with st.expander(f"📈 {row['Symbol']} ({row.get('Company', '')}) Chart"):
                    plot_stock_chart(row['Symbol'])

            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results", csv, "smart_stock_results.csv", "text/csv")
        else:
            st.warning("No matching stocks found.")
