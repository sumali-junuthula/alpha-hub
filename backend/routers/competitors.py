from fastapi import APIRouter, Query, HTTPException
import requests
import os
from dotenv import load_dotenv
from config import FMP_API_KEY

load_dotenv()
router = APIRouter()

@router.get("/")
def get_competitor_signals(ticker: str = Query(..., min_length=1)):
  try:
    profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
    profile_res = requests.get(profile_url).json()
    
    if not profile_res or "industry" not in profile_res[0]:
      raise HTTPException(status_code=404, detail="Could not resolve industry.")

    industry = profile_res[0]["industry"]

    # Get competitors in the same industry
    screener_url = f"https://financialmodelingprep.com/api/v3/stock-screener?industry={industry}&limit=10&apikey={FMP_API_KEY}"
    screener_res = requests.get(screener_url).json()

    competitors = []
    for comp in screener_res:
      if comp["symbol"].lower() == ticker.lower():
        continue
      competitors.append({
        "name": comp["companyName"],
        "ticker": comp["symbol"],
        "price": comp["price"],
        "changesPercentage": comp.get("changesPercentage", "0%"),
        "exchange": comp["exchangeShortName"]
      })

    return {"industry": industry, "competitors": competitors[:5]}
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error fetching competitors: {str(e)}")
