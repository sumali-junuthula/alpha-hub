from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ForecastResponse(BaseModel):
  dates: List[str]
  prices: List[float]

@router.get("/", response_model=ForecastResponse)
def get_forecast(ticker: str = Query(..., description="Stock ticker")):
  # TODO: Replace with real forecast logic
  return {
    "dates": ["2025-06-08", "2025-06-09", "2025-06-10"],
    "prices": [192.4, 194.8, 198.1],
  }
