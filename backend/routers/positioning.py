from fastapi import APIRouter, Query
from services.positioning import get_positioning_data

router = APIRouter()

@router.get("/")
def get_positioning(ticker: str = Query(..., description="Stock ticker")):
  return get_positioning_data(ticker)
