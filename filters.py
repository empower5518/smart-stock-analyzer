import pandas as pd

def apply_all_filters(price_range, min_roe, max_de_ratio, rsi_threshold, beta_threshold, market_caps, sector_filter):
    data = [
        {"Symbol": "TCS", "Company": "Tata Consultancy", "Price": 720, "ROE": 25, "DebtEquity": 0.1, "RSI": 62, "Beta": 1.1, "MarketCapCategory": "Largecap", "Sector": "IT"},
        {"Symbol": "CLEAN", "Company": "Clean Science", "Price": 530, "ROE": 18, "DebtEquity": 0.2, "RSI": 66, "Beta": 1.0, "MarketCapCategory": "Midcap", "Sector": "Chemicals"},
    ]
    df = pd.DataFrame(data)

    filtered = df[
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['ROE'] >= min_roe) &
        (df['DebtEquity'] <= max_de_ratio) &
        (df['RSI'] >= rsi_threshold) &
        (df['Beta'] <= beta_threshold) &
        (df['MarketCapCategory'].isin(market_caps))
    ]

    if sector_filter:
        filtered = filtered[filtered['Sector'].str.contains(sector_filter, case=False)]

    return filtered.reset_index(drop=True)
