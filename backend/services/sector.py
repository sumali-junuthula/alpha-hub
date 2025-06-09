# services/sector.py
import requests
import os
from dotenv import load_dotenv
from config import NEWS_API_KEY

load_dotenv()

macro_keywords = ["interest rates", "inflation", "recession", "GDP growth", "sector outlook"]

def get_sector_commentary(sector_name):
  query = f"{sector_name} {' OR '.join(macro_keywords)}"
  url = "https://newsapi.org/v2/everything"
  params = {
    "q": query,
    "sortBy": "relevancy",
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
    raise RuntimeError(f"Macro summary fetch error: {e}")
