import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_stock_data(symbol):
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        info = ticker.info
        hist = ticker.history(period="6mo")

        roe = info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else 0
        debt_equity = info.get("debtToEquity", 0) / 100 if info.get("debtToEquity") else 0
        beta = info.get("beta", 1.0)
        price = info.get("currentPrice", 0)

        # Calculate RSI (14-day)
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        latest_rsi = round(rsi.iloc[-1], 2) if not rsi.empty else 50

        return {
            "Symbol": symbol,
            "Company": info.get("shortName", symbol),
            "Price": price,
            "ROE": round(roe, 2),
            "DebtEquity": round(debt_equity, 2),
            "RSI": latest_rsi,
            "Beta": round(beta, 2),
            "History": hist
        }

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def fetch_sector_and_marketcap(symbol):
    try:
        url = f"https://www.screener.in/company/{symbol}/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sector
        sector_tag = soup.select_one(".company-profile .sub:nth-of-type(2)")
        sector = sector_tag.text.strip() if sector_tag else "Unknown"

        # Market Cap Category (based on scraped ₹ value in Cr.)
        market_cap_tag = soup.find("li", string=lambda t: t and "Market Cap" in t)
        if market_cap_tag:
            text = market_cap_tag.text
            if "Cr." in text:
                value = float(text.split(':')[1].replace('Cr.', '').replace(',', '').strip())
                if value < 5000:
                    category = "Smallcap"
                elif value < 20000:
                    category = "Midcap"
                else:
                    category = "Largecap"
            else:
                category = "Midcap"
        else:
            category = "Midcap"

        return sector, category

    except Exception as e:
        print(f"Error fetching Screener data for {symbol}: {e}")
        return "Unknown", "Midcap"
