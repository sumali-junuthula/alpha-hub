from fastapi import APIRouter, Query
from services.reddit import fetch_reddit_posts

router = APIRouter()

@router.get("/")
async def reddit(ticker: str = Query(...)):
  return fetch_reddit_posts(ticker)
