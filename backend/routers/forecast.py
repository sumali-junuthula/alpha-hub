import yfinance as yf
from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
import datetime
import numpy as np

router = APIRouter()

class ForecastResponse(BaseModel):
  dates: List[str]
  prices: List[float]

@router.get("/", response_model=ForecastResponse)
def get_forecast(ticker: str = Query(..., description="Stock ticker")):
  stock = yf.Ticker(ticker)
  current_price = stock.history(period="1d")["Close"][-1]

  np.random.seed(abs(hash(ticker)) % (10 ** 8))

  today = datetime.date.today()
  dates = [(today + datetime.timedelta(days=i)).isoformat() for i in range(14)]

  daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=14)
  prices = [current_price]

  for r in daily_returns:
      prices.append(prices[-1] * (1 + r))

  prices = [round(p, 2) for p in prices[1:]]

  return {
    "dates": dates,
    "prices": prices,
  }
  
