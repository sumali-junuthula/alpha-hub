import pandas as pd
from pytrends.request import TrendReq
from config import TIMEFRAME, TRENDS_KEYWORD, TRENDS_TIMEFRAME, TRENDS_TIMEZONE


def fetch_trends(keyword=TRENDS_KEYWORD):
  pytrends = TrendReq(hl='en-US', tz=TRENDS_TIMEZONE)
  pytrends.build_payload([keyword], cat=0, timeframe=TRENDS_TIMEFRAME, geo='', gprop='')

  df = pytrends.interest_over_time()
  df = df.reset_index()
  df.to_csv("data/output/trends.csv", index=False)
  print(f"Saved Google Trends data to data/output/trends.csv")

if __name__ == "__main__":
  fetch_trends()
