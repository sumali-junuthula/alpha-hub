import os
import requests
from urllib.parse import urlparse
from datetime import datetime
from dotenv import load_dotenv
from config import NEWS_API_KEY

load_dotenv()

def is_valid_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc]) and not url.endswith(".pdf")
  except:
    return False

def format_date(date_str):
  try:
    if not date_str:
      return "Date Unknown"
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return dt.strftime("%b %d, %Y")
  except Exception:
    return "Date Unknown"


def get_news_articles(ticker):
  url = "https://newsapi.org/v2/everything"
  params = {
    "q": f"{ticker} company stock",
    "language": "en",
    "sortBy": "relevancy",
    "pageSize": 10,
    "apiKey": NEWS_API_KEY,
  }

  response = requests.get(url, params=params)
  articles = response.json().get("articles", [])

  clean_articles = []
  for a in articles:
    if not a.get("title") or not is_valid_url(a.get("url", "")):
      continue
    if "newsapi.org" in a["url"] or "example.com" in a["url"]:
      continue

    clean_articles.append({
      "title": a["title"],
      "description": a.get("description", "").strip() or "No summary available.",
      "url": a["url"],
      "publishedAt": format_date(a.get("publishedAt", "")),
    })

  return clean_articles[:5]
