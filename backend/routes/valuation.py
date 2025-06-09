from fastapi import APIRouter, Query, HTTPException
from services.valuation import build_valuation_model

router = APIRouter()

@router.get("/")
def get_valuation(ticker: str = Query(...)):
  try:
    valuation = build_valuation_model(ticker)
    dcf = build_valuation_model(ticker)
    valuation["valuation_summary"]["dcf_summary"] = dcf
    return valuation
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
