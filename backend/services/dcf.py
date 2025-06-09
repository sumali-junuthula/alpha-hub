import os
import math
import requests
from dotenv import load_dotenv
from config import FMP_API_KEY, FMP_URL

load_dotenv()

def get_json(url):
  res = requests.get(url)
  res.raise_for_status()
  return res.json()

def fetch_free_cash_flow(ticker):
  url = f"{FMP_URL}/cash-flow-statement/{ticker}?limit=5&apikey={FMP_API_KEY}"
  data = get_json(url)
  if not data or len(data) < 2:
    return None, None
  last_cf = float(data[0]["freeCashFlow"])
  prev_cf = float(data[1]["freeCashFlow"])
  growth_rate = (last_cf - prev_cf) / abs(prev_cf)
  return last_cf, round(growth_rate, 3)

def fetch_wacc(ticker):
  url = f"{FMP_URL}/company-key-metrics-ttm/{ticker}?apikey={FMP_API_KEY}"
  data = get_json(url)
  if data and isinstance(data, list):
    return float(data[0].get("wacc", 0.10))
  return 0.10

def calculate_dcf(ticker):
  # 1. Pull historical free cash flow
  url = f"{FMP_URL}/cash-flow-statement/{ticker}?limit=5&apikey={FMP_API_KEY}"
  data = get_json(url)

  fcfs = [float(entry.get("freeCashFlow", 0)) for entry in reversed(data)]
  if not fcfs or len(fcfs) < 5:
    raise ValueError("Insufficient FCF data.")

  # 2. Compute 5-year CAGR
  start, end = fcfs[0], fcfs[-1]
  growth_rate = ((end / start) ** (1 / 4)) - 1 if start > 0 else 0.08
  projected_fcfs = [fcfs[-1] * (1 + growth_rate) ** i for i in range(1, 6)]

  # 3. Estimate WACC (placeholder value for now)
  wacc = 0.085  # Could improve using capital structure later
  terminal_growth_rate = 0.025

  # 4. Discount projected FCFs
  npv = sum(fcf / (1 + wacc) ** i for i, fcf in enumerate(projected_fcfs, 1))

  # 5. Terminal value
  terminal_value = projected_fcfs[-1] * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)
  terminal_npv = terminal_value / (1 + wacc) ** len(projected_fcfs)

  total_dcf = npv + terminal_npv

  return {
    "dcf_summary": {
      "projected_fcfs": projected_fcfs,
      "growth_rate": round(growth_rate, 4),
      "discount_rate": wacc,
      "terminal_growth_rate": terminal_growth_rate,
      "terminal_value": terminal_value,
      "present_value_of_fcfs": npv,
      "present_value_of_terminal": terminal_npv,
      "total_dcf_valuation": total_dcf
    }
  }
