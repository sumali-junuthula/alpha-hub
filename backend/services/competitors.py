import os
import requests
from dotenv import load_dotenv
from config import FMP_API_KEY

load_dotenv()

def fetch_competitor_signal(ticker: str):
  profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
  profile_res = requests.get(profile_url).json()
  
  if not profile_res or "industry" not in profile_res[0]:
    raise ValueError("Could not resolve industry.")

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

  return {
    "industry": industry,
    "competitors": competitors[:5]
  }
