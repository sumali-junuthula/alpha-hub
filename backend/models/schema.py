from pydantic import BaseModel
from typing import List

class PricePoint(BaseModel):
    date: str
    close: float

class CompanyInfo(BaseModel):
    ticker: str
    name: str
    sector: str
    industry: str
    description: str
    price_history: List[PricePoint]

class ForecastPoint(BaseModel):
    date: str
    predicted_return: float  # percent return
    confidence: float

class ForecastResponse(BaseModel):
    ticker: str
    forecast: List[ForecastPoint]
