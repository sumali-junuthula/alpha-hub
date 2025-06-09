from fastapi import APIRouter, Query, HTTPException
from pytrends.request import TrendReq
import requests
from datetime import datetime, timedelta

router = APIRouter()

def resolve_company_name(ticker: str) -> str:
  url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}"
  try:
    res = requests.get(url)
    res.raise_for_status()
    quotes = res.json().get("quotes", [])
    for q in quotes:
      if q.get("symbol", "").upper() == ticker.upper():
        return q.get("shortname") or ticker
    return ticker
  except:
    return ticker

@router.get("/")
def get_google_trends(ticker: str = Query(...)):
  company_name = resolve_company_name(ticker)

  pytrends = TrendReq(hl='en-US', tz=360)
  pytrends.build_payload([company_name], cat=0, timeframe='now 7-d', geo='US')

  try:
    df = pytrends.interest_over_time()
    if df.empty:
      raise HTTPException(status_code=404, detail="No trend data found.")

    dates = [d.strftime("%Y-%m-%d") for d in df.index]
    values = df[company_name].tolist()

    return {
      "ticker": ticker.upper(),
      "company": company_name,
      "dates": dates,
      "interest": values
    }

  except Exception as e:
    print("❌ Google Trends fetch error:", str(e))
    raise HTTPException(status_code=500, detail="Error fetching Google Trends data.")
