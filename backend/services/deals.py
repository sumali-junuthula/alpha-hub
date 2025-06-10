import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import NEWS_API_KEY

load_dotenv()

def get_recent_deals(ticker_or_name):
  """
  Uses NewsAPI to get M&A-related top headlines for a company.
  Works on the free tier by using /v2/top-headlines and a simple query.
  """
  query = ticker_or_name

  url = "https://newsapi.org/v2/everything"
  params = {
    "q": query,
    "language": "en",
    "pageSize": 10,
    "apiKey": NEWS_API_KEY
  }

  try:
    res = requests.get(url, params=params)
    res.raise_for_status()
    articles = res.json().get("articles", [])

    return [
      {
        "title": a["title"],
        "source": a["source"]["name"],
        "published": a["publishedAt"][:10],
        "url": a["url"]
      }
      for a in articles
    ]

  except Exception as e:
    raise RuntimeError(f"Deal radar fetch error: {e}")

