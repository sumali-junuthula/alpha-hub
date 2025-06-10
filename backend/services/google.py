import time
import random
from pytrends.request import TrendReq
from datetime import datetime, timedelta
from typing import Dict

# In-memory cache to avoid refetching during the same session
TREND_CACHE: Dict[str, Dict] = {}

def fetch_google_trends(ticker: str):
  today = datetime.today().date()
  cache_key = f"{ticker}_{today.isoformat()}"

  # ✅ Return from cache if available
  if cache_key in TREND_CACHE:
    return TREND_CACHE[cache_key]

  # ✅ Set up pytrends with retries
  pytrends = TrendReq(hl='en-US', tz=360, retries=3, backoff_factor=0.5)

  # ✅ Randomized delay to avoid 429
  time.sleep(random.uniform(2.0, 5.0))

  try:
    last_3_months = today - timedelta(days=90)
    timeframe = f"{last_3_months.strftime('%Y-%m-%d')} {today.strftime('%Y-%m-%d')}"
    
    pytrends.build_payload([ticker], cat=0, timeframe=timeframe, geo='', gprop='')
    data = pytrends.interest_over_time()

    if data.empty:
      result = {
        "ticker": ticker,
        "company": ticker,
        "interest": [],
        "dates": [],
        "error": "No data found for given ticker"
      }
    else:
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

  # ✅ Cache result for this ticker/date
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
