import os
import time
import requests
from dotenv import load_dotenv
from services.dcf import calculate_dcf
from config import FMP_API_KEY, FMP_URL

load_dotenv()

# --- Caching layer ---
cache = {}

def get_json_cached(url, cache_key):
  if cache_key in cache:
    return cache[cache_key]
  res = requests.get(url)
  res.raise_for_status()
  data = res.json()
  cache[cache_key] = data
  return data

def get_company_profile(ticker):
  url = f"{FMP_URL}/profile/{ticker}?apikey={FMP_API_KEY}"
  return get_json_cached(url, f"profile_{ticker}")[0]

def get_ratios(ticker):
  url = f"{FMP_URL}/ratios-ttm/{ticker}?apikey={FMP_API_KEY}"
  return get_json_cached(url, f"ratios_{ticker}")[0]

def get_income_statement(ticker):
  url = f"{FMP_URL}/income-statement/{ticker}?limit=1&apikey={FMP_API_KEY}"
  return get_json_cached(url, f"income_{ticker}")[0]

def get_enterprise_value(ticker):
  url = f"{FMP_URL}/enterprise-values/{ticker}?limit=1&apikey={FMP_API_KEY}"
  return get_json_cached(url, f"ev_{ticker}")[0]

def get_comps_by_industry(industry, exclude_ticker=None, limit=5):
  url = f"{FMP_URL}/stock-screener?industry={industry}&limit={limit}&apikey={FMP_API_KEY}"
  data = get_json_cached(url, f"comps_{industry}")
  return [c for c in data if c["symbol"].lower() != exclude_ticker.lower()]

def generate_llm_summary(name, industry, pe_val, ebitda_val, sales_val):
  return (
    f"{name}, operating in the {industry} sector, is valued at approximately "
    f"${pe_val/1e9:.1f}B (P/E), ${ebitda_val/1e9:.1f}B (EV/EBITDA), and "
    f"${sales_val/1e9:.1f}B (EV/Sales), suggesting a balanced market position with "
    f"potential upside if EBITDA margins continue to outperform peers."
  )

def median_or_average(data, key):
  values = [d[key] for d in data if d.get(key, 0) > 0]
  if not values:
    return 1
  values.sort()
  n = len(values)
  return values[n // 2] if n % 2 == 1 else (values[n // 2 - 1] + values[n // 2]) / 2

def build_valuation_model(ticker):
  profile = get_company_profile(ticker)
  ratios = get_ratios(ticker)
  income = get_income_statement(ticker)
  ev_data = get_enterprise_value(ticker)

  company_name = profile.get("companyName", "")
  industry = profile.get("industry", "")
  shares_out = profile.get("sharesOutstanding", 1)

  comps = get_comps_by_industry(industry, exclude_ticker=ticker)

  peer_data = []
  for comp in comps:
    symbol = comp["symbol"]
    try:
      time.sleep(0.5)  # Respectful delay
      r = get_ratios(symbol)
      peer_data.append({
        "ticker": symbol,
        "name": comp.get("companyName", ""),
        "pe": float(r.get("priceEarningsRatioTTM", 0)),
        "ev_ebitda": float(r.get("evToEbitdaTTM", 0)),
        "ev_sales": float(r.get("evToSalesTTM", 0)),
        "market_cap": comp.get("marketCap", 0)
      })
    except Exception:
      continue

  # Current ratios
  pe = float(ratios.get("priceEarningsRatioTTM", 0))
  ev_ebitda = float(ratios.get("evToEbitdaTTM", 0))
  ev_sales = float(ratios.get("evToSalesTTM", 0))

  # Financials
  ebitda = float(income.get("ebitda", 0))
  net_income = float(income.get("netIncome", 0))
  revenue = float(income.get("revenue", 0))

  net_debt = float(ev_data.get("totalDebt", 0)) - float(ev_data.get("cashAndShortTermInvestments", 0))

  # Valuation calculations
  pe_equity = net_income * median_or_average(peer_data, "pe")
  ev_ebitda_val = ebitda * median_or_average(peer_data, "ev_ebitda")
  ev_sales_val = revenue * median_or_average(peer_data, "ev_sales")

  # Convert EV to equity
  ebitda_equity = ev_ebitda_val - net_debt
  sales_equity = ev_sales_val - net_debt

  # DCF block
  dcf = calculate_dcf(ticker)

  return {
    "ticker": ticker.upper(),
    "company_name": company_name,
    "industry": industry,
    "peer_multiples": peer_data,
    "target_multiples": {
      "pe": pe,
      "ev_ebitda": ev_ebitda,
      "ev_sales": ev_sales,
      "ebitda": ebitda,
      "net_income": net_income,
      "revenue": revenue,
      "shares_outstanding": shares_out
    },
    "valuation_summary": {
      "pe_implied_equity": pe_equity,
      "ev_ebitda_implied_ev": ev_ebitda_val,
      "ev_sales_implied_ev": ev_sales_val,
      "ev_to_equity_conversion": {
        "net_debt": net_debt,
        "equity_from_ev": True
      },
      "share_price_range": {
        "pe_based": round(pe_equity / shares_out, 2),
        "ebitda_based": round(ebitda_equity / shares_out, 2),
        "sales_based": round(sales_equity / shares_out, 2)
      },
      "dcf_summary": dcf["dcf_summary"]
    },
    "discounted_cash_flow": {
      "enterprise_value": ev_ebitda_val,
      "equity_value": ebitda_equity,
      "share_price": round(ebitda_equity / shares_out, 2)
    },
    "sensitivity_matrix": [
      ["", "10x", "12x", "14x"],
      ["$100B", "$120B", "$140B"],
      ["$120B", "$144B", "$168B"],
      ["$140B", "$168B", "$196B"]
    ],
    "summary": generate_llm_summary(company_name, industry, pe_equity, ev_ebitda_val, ev_sales_val)
  }
