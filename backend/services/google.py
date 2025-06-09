from pytrends.request import TrendReq
from datetime import datetime, timedelta

def fetch_google_trends(ticker: str):
  pytrends = TrendReq(hl='en-US', tz=360)
  
  today = datetime.today()
  last_3_months = today - timedelta(days=90)
  timeframe = f"{last_3_months.strftime('%Y-%m-%d')} {today.strftime('%Y-%m-%d')}"
  
  pytrends.build_payload([ticker], cat=0, timeframe=timeframe, geo='', gprop='')
  data = pytrends.interest_over_time()

  if data.empty:
    return {
      "ticker": ticker,
      "interest_over_time": [],
      "dates": []
    }

  interest = data[ticker].tolist()
  dates = data.index.strftime('%Y-%m-%d').tolist()

  return {
    "ticker": ticker,
    "interest_over_time": interest,
    "dates": dates
  }