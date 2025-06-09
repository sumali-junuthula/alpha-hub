from fastapi import APIRouter, HTTPException, Query
from services.earnings import analyze_earnings_sentiment

router = APIRouter()

@router.get("/")
def earnings_sentiment(ticker: str = Query(...)):
  try:
    return analyze_earnings_sentiment(ticker)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
