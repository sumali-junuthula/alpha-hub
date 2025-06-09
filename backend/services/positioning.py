import os
import requests
from dotenv import load_dotenv
from config import FMP_API_KEY, FMP_URL

load_dotenv()

def get_positioning_data(ticker: str):
  income_url = f"{FMP_URL}/income-statement/{ticker}?limit=2&apikey={FMP_API_KEY}"
  profile_url = f"{FMP_URL}/profile/{ticker}?apikey={FMP_API_KEY}"
  ratios_url = f"{FMP_URL}/ratios-ttm/{ticker}?apikey={FMP_API_KEY}"

  try:
    income_data = requests.get(income_url).json()
    profile_data = requests.get(profile_url).json()
    ratios_data = requests.get(ratios_url).json()

    if not income_data or not profile_data or not ratios_data:
      raise ValueError("Missing data from FMP")

    income_now = income_data[0]
    income_prev = income_data[1] if len(income_data) > 1 else income_data[0]
    ratios = ratios_data[0]

    revenue_now = float(income_now.get("revenue", 0))
    revenue_prev = float(income_prev.get("revenue", 1)) or 1  # avoid div 0
    net_income = float(income_now.get("netIncome", 0))
    ebitda = float(income_now.get("ebitda", 0))

    # Key Metrics
    growth = ((revenue_now - revenue_prev) / revenue_prev) * 10
    profitability = (net_income / revenue_now) * 10 if revenue_now else 0
    valuation = float(ratios.get("priceEarningsRatioTTM", 10))
    efficiency = float(ratios.get("returnOnEquityTTM", 10))
    market_cap = float(profile_data[0].get("mktCap", 1))

    return {
      "ticker": ticker.upper(),
      "positioning": {
        "growth": round(growth, 2),
        "profitability": round(profitability, 2),
        "market_share": round(market_cap / 1e11, 2),  # relative scaling
        "efficiency": round(efficiency, 2),
        "valuation": round(valuation, 2)
      }
    }

  except Exception as e:
    return {
      "ticker": ticker.upper(),
      "positioning": {
        "growth": 0,
        "profitability": 0,
        "market_share": 0,
        "efficiency": 0,
        "valuation": 0
      },
      "error": f"Positioning fetch error: {str(e)}"
    }
