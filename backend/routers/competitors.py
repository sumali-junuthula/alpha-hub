from fastapi import APIRouter, Query, HTTPException
from services.competitors import fetch_competitor_signal

router = APIRouter()

@router.get("/")
def get_competitor_signals(ticker: str = Query(..., min_length=1)):
  try:
    return fetch_competitor_signal(ticker)
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error fetching competitors: {str(e)}")
