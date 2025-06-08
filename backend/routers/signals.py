from fastapi import APIRouter, Query
from typing import List

router = APIRouter()

@router.get("/reddit/")
def get_reddit(ticker: str):
  return {
    "sentiment": 0.73,
    "posts": [
      {"title": f"{ticker} is going to the moon!", "upvotes": 231, "date": "2025-06-08"},
      {"title": f"Bearish take on {ticker}", "upvotes": 102, "date": "2025-06-07"}
    ]
  }

@router.get("/news/")
def get_news(ticker: str):
  return {
    "articles": [
      {"title": f"{ticker} signs $1B AI partnership", "summary": "Massive strategic expansion into cloud AI."},
      {"title": f"{ticker} Q2 earnings beat estimates", "summary": "Strong revenue growth driven by services."}
    ]
  }

@router.get("/google-trends/")
def get_trends(ticker: str):
  return {
    "summary": f"{ticker} search volume up 35% in the last 7 days.",
    "trend": [24, 30, 40, 60, 55, 70, 80]
  }

@router.get("/competitors/")
def get_competitors(ticker: str):
  return {
    "names": ["GOOGL", "MSFT", "NVDA"],
    "prices": [180.3, 325.6, 1132.4]
  }

@router.get("/satellite/")
def get_satellite(ticker: str):
  return {
    "signal": 0.87,
    "summary": f"Satellite imagery suggests higher-than-expected store traffic for {ticker}."
  }
