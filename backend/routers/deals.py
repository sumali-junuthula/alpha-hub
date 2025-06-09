from fastapi import APIRouter, HTTPException, Query
from services.deal_radar import get_recent_deals

router = APIRouter()

@router.get("/")
def fetch_deals(ticker: str = Query(...)):
  try:
    results = get_recent_deals(ticker)
    return {"company": ticker, "deals": results}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
