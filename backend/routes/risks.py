from fastapi import APIRouter, Query, HTTPException
from services.risks import get_risk_analysis

router = APIRouter()

@router.get("/")
def get_risk(ticker: str = Query(...)):
  try:
    return get_risk_analysis(ticker)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
