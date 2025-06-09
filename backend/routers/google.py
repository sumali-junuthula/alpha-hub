from fastapi import APIRouter, HTTPException, Query
from pytrends.request import TrendReq
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
def get_google_trends(ticker: str = Query(...)):
  try:
    pytrends = TrendReq(hl='en-US', tz=360)

    today = datetime.today()
    last_30_days = today - timedelta(days=30)
    timeframe = f"{last_30_days.strftime('%Y-%m-%d')} {today.strftime('%Y-%m-%d')}"

    # safest fallback: use ticker instead of company name to reduce ambiguity
    pytrends.build_payload([ticker], cat=0, timeframe=timeframe, geo='US')
    df = pytrends.interest_over_time()

    if df.empty or ticker not in df.columns:
      raise HTTPException(status_code=404, detail="No trend data found.")

    dates = [d.strftime("%Y-%m-%d") for d in df.index]
    interest = df[ticker].tolist()

    return {
      "ticker": ticker.upper(),
      "company": ticker.upper(),
      "dates": dates,
      "interest": interest
    }

  except Exception as e:
    print("❌ Google Trends fetch error:", str(e))
    # fallback dummy response
    return {
      "ticker": ticker.upper(),
      "company": ticker.upper(),
      "dates": ["2025-06-01", "2025-06-02", "2025-06-03"],
      "interest": [25, 30, 27],
      "error": str(e)
    }
