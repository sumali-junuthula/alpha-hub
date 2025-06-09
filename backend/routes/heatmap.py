from fastapi import APIRouter, Query, HTTPException
from services.heatmap import get_positioning_heatmap
from services.valuation import get_company_profile

router = APIRouter()

@router.get("/")
def fetch_heatmap(ticker: str = Query(...)):
  try:
    profile = get_company_profile(ticker)
    industry = profile.get("industry", "")
    data = get_positioning_heatmap(ticker, industry)
    return {"ticker": ticker.upper(), "heatmap": data}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
