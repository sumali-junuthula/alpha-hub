import time
import random
from pytrends.request import TrendReq
from datetime import datetime, timedelta
from typing import Dict

TREND_CACHE: Dict[str, Dict] = {}

def fetch_google_trends(ticker: str):
  today = datetime.today().date()
  cache_key = f"{ticker}_{today.isoformat()}"

  if cache_key in TREND_CACHE:
    return TREND_CACHE[cache_key]

  try:
    # Wait randomly to avoid detection
    time.sleep(random.uniform(2.0, 5.0))

    pytrends = TrendReq(
      hl='en-US',
      tz=360,
      retries=5,
      backoff_factor=0.7
    )

    last_3_months = today - timedelta(days=90)
    timeframe = f"{last_3_months} {today}"

    pytrends.build_payload([ticker], cat=0, timeframe=timeframe, geo='', gprop='')
    data = pytrends.interest_over_time()

    if data.empty:
      raise ValueError("No data returned from Google Trends")

    interest = data[ticker].tolist()
    dates = data.index.strftime('%Y-%m-%d').tolist()

    result = {
      "ticker": ticker,
      "company": ticker,
      "interest": interest,
      "dates": dates
    }

  except Exception as e:
    result = {
      "ticker": ticker,
      "company": ticker,
      "interest": [],
      "dates": [],
      "error": f"The request failed: {str(e)}"
    }

  TREND_CACHE[cache_key] = result
  return result

# import time
# from pytrends.request import TrendReq
# from datetime import datetime, timedelta

# def fetch_google_trends(ticker: str):
#   pytrends = TrendReq(hl='en-US', tz=360)
#   time.sleep(5)
  
#   today = datetime.today()
#   last_3_months = today - timedelta(days=90)
#   timeframe = f"{last_3_months.strftime('%Y-%m-%d')} {today.strftime('%Y-%m-%d')}"
  
#   pytrends.build_payload([ticker], cat=0, timeframe=timeframe, geo='', gprop='')
#   data = pytrends.interest_over_time()

#   if data.empty:
#     return {
#       "ticker": ticker,
#       "interest_over_time": [],
#       "dates": []
#     }

#   interest = data[ticker].tolist()
#   dates = data.index.strftime('%Y-%m-%d').tolist()

#   return {
#     "ticker": ticker,
#     "interest_over_time": interest,
#     "dates": dates
#   }
