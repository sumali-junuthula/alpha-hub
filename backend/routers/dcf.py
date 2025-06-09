from fastapi import APIRouter, Query, HTTPException
from services.dcf import calculate_dcf

router = APIRouter()

@router.get("/")
def get_dcf(ticker: str = Query(...)):
  try:
    return calculate_dcf(ticker)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
