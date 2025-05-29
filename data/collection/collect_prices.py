import yfinance as yf
import pandas as pd
from config import PRICE_TICKER, PRICE_START_DATE, PRICE_END_DATE

def fetch_stock(ticker=PRICE_TICKER, start=PRICE_START_DATE, end=PRICE_END_DATE):
  df = yf.download(ticker, start=start, end=end, interval="1d")
  df.reset_index(inplace=True)
  df.to_csv("data/output/prices.csv", index=False)
  print(f"Saved {len(df)} stock price rows to data/output/prices.csv")

if __name__ == "__main__":
  fetch_stock()
