from fastapi import APIRouter, Query
from services.explainer import explain_forecast

router = APIRouter()

@router.get("/")
def explain(ticker: str = Query(...)):
  return explain_forecast(ticker)
