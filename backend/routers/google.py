from fastapi import APIRouter, Query
from services.google import fetch_google_trends

router = APIRouter()

@router.get("/")
def get_google_trends(ticker: str = Query(...)):
  return fetch_google_trends(ticker)
