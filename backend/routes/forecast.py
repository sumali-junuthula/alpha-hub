from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ForecastResponse(BaseModel):
  dates: List[str]
  prices: List[float]

@router.get("/", response_model=ForecastResponse)
def get_forecast(ticker: str = Query(..., description="Stock ticker")):
  # Just return mock data based on ticker hash
  import hashlib
  import datetime

  # Deterministic hash to vary prices per ticker
  base = sum(bytearray(ticker.encode())) % 100 + 100

  today = datetime.date.today()
  dates = [(today + datetime.timedelta(days=i)).isoformat() for i in range(3)]
  prices = [round(base + i * 2 + (i % 2) * 0.4, 2) for i in range(3)]

  return {
    "dates": dates,
    "prices": prices,
  }
