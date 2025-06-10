from fastapi import APIRouter, Query, HTTPException
from services.satellite import fetch_satellite_data, extract_competitor_insight

router = APIRouter()

@router.get("/satellite/")
def get_satellite_insight(ticker: str = Query(..., description="Stock ticker")):
  raw_data = fetch_satellite_data(ticker)
  if not raw_data:
    raise HTTPException(status_code=500, detail="Failed to fetch satellite data.")

  insight = extract_competitor_insight(raw_data)
  return insight
