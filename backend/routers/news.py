# backend/routes/news.py
from fastapi import APIRouter, Query
from services.news import get_news_articles

router = APIRouter()

@router.get("/")
async def news(ticker: str = Query(...)):
  return get_news_articles(ticker)
