import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Query, HTTPException
from config import FMP_API_KEY

router = APIRouter()

@router.get("/")
def resolve_ticker(query: str = Query(...)):
  url = f"https://financialmodelingprep.com/api/v3/search?query={query}&limit=20&apikey={FMP_API_KEY}"
  print(f"🔍 Requesting: {url}")

  try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    results = response.json()

    if not results:
      raise HTTPException(status_code=404, detail="No matching ticker found.")
    
    query_lower = query.lower()

    exact = next((r for r in results if r["name"].lower() == query_lower), None)
    if exact:
      return {"ticker": exact["symbol"]}
    
    partial = next(
      (r for r in results if query_lower in r["name"].lower() and r["exchangeShortName"] in {"NYSE", "NASDAQ"}),
      None,
    )
    if partial:
      return {"ticker": partial["symbol"]}

    # ✅ Fallback to US-based stock
    us_based = next((r for r in results if r["exchangeShortName"] in {"NYSE", "NASDAQ"}), None)
    if us_based:
      return {"ticker": us_based["symbol"]}
    
    return {"ticker": results[0]["symbol"]}
  
  except Exception as e:
    print("❌ FMP Resolve Error:", str(e))
    raise HTTPException(status_code=500, detail=f"Resolve error: {str(e)}")
