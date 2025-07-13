import pandas as pd
from data_fetcher import fetch_stock_data, fetch_sector_and_marketcap
from utils import is_bouncing_from_bottom, has_volume_spike

def apply_all_filters(price_range, min_roe, max_de_ratio, rsi_threshold, beta_threshold, market_caps, sector_filter):
    stock_symbols = ["TCS", "INFY", "CLEAN", "HDFCBANK", "LT", "PIDILITIND", "AARTIIND", "APOLLOHOSP", "COFORGE", "ICICIBANK", "TATAMOTORS", "AMARAJABAT"]
    results = []

    for symbol in stock_symbols:
        data = fetch_stock_data(symbol)
        if not data:
            continue

        hist = data.get("History")
        if hist is None or hist.empty:
            continue

        if not is_bouncing_from_bottom(hist):
            continue

        if not has_volume_spike(hist):
            continue

        if (
            price_range[0] <= data['Price'] <= price_range[1] and
            data['ROE'] >= min_roe and
            data['DebtEquity'] <= max_de_ratio and
            data['RSI'] >= rsi_threshold and
            data['Beta'] <= beta_threshold
        ):
            sector, cap_category = fetch_sector_and_marketcap(symbol)
            data['Sector'] = sector or "Unknown"
            data['MarketCapCategory'] = cap_category or "Midcap"

            if sector_filter and sector_filter.lower() not in data['Sector'].lower():
                continue

            if cap_category and cap_category not in market_caps:
                continue

            results.append(data)

    return pd.DataFrame(results)
