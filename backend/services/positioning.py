import os
import requests
from dotenv import load_dotenv
from config import FMP_URL, FMP_API_KEY_POS

# Load API key from .env file
load_dotenv()

def normalize(value, min_val, max_val):
  return round(max(0, min(1, (value - min_val) / (max_val - min_val))), 2)

def hybrid_normalize(value, peer_avg, abs_min, abs_max, weight=0.6):
  abs_score = normalize(value, abs_min, max(abs_max, abs_min + 1e-6))
  rel_score = min(max(value / peer_avg, 0), 1.5) if peer_avg else 0
  return round(weight * abs_score + (1 - weight) * rel_score, 2)

def fetch_data(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
    return None
  except:
    return None

def fetch_financials(ticker):
  income_url = f"{FMP_URL}/income-statement/{ticker}?limit=2&apikey={FMP_API_KEY}"
  profile_url = f"{FMP_URL}/profile/{ticker}?apikey={FMP_API_KEY}"
  ratios_url = f"{FMP_URL}/ratios-ttm/{ticker}?apikey={FMP_API_KEY}"

  income_data = fetch_data(income_url)
  profile_data = fetch_data(profile_url)
  ratios_data = fetch_data(ratios_url)

  if not income_data or not profile_data or not ratios_data:
    raise ValueError("Missing data from FMP")

  profile = profile_data[0]
  sector = profile.get("sector", "Unknown")
  market_cap = float(profile.get("mktCap", 0))

  return income_data, ratios_data, market_cap, sector

def get_sector_benchmarks(sector):
  # Conservative default benchmarks — can be replaced with live peer averaging
  return {
    "growth": 6.5,             # Revenue growth in %
    "net_margin": 7.0,         # Net income margin in %
    "roe": 18.0,               # Return on Equity in %
    "market_cap": 150e9        # USD
  }

def get_positioning_data(ticker):
  try:
    income, ratios, market_cap, sector = fetch_financials(ticker)
    sector_avg = get_sector_benchmarks(sector)

    revenue_now = float(income[0]["revenue"])
    revenue_prev = float(income[1]["revenue"]) if len(income) > 1 else revenue_now
    net_income = float(income[0]["netIncome"])
    pe_ratio = float(ratios[0].get("priceEarningsRatioTTM", 20))

    roe_raw = ratios[0].get("returnOnEquityTTM")
    try:
      roe = float(roe_raw)
      if roe < 1:  # likely decimal format, convert to %
        roe *= 100
    except:
      roe = 0.0

    growth_rate = ((revenue_now - revenue_prev) / revenue_prev) * 100 if revenue_prev else 0
    net_margin = (net_income / revenue_now) * 100 if revenue_now else 0

    return {
      "ticker": ticker.upper(),
      "positioning": {
        "growth": hybrid_normalize(growth_rate, sector_avg["growth"], 0, 20),
        "profitability": min(hybrid_normalize(net_margin, sector_avg["net_margin"], 0, 30), 1.0),
        "market_share": min(hybrid_normalize(market_cap, sector_avg["market_cap"], 1e9, 3e12), 1.0),
        "efficiency": min(hybrid_normalize(roe, sector_avg["roe"], 0, 50), 1.0),
        "valuation": round(pe_ratio, 2)
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
    