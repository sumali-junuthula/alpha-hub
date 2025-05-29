import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import TIMEFRAME, NEWS_QUERY, NEWS_FROM_DATE, NEWS_TO_DATE, NEWS_PAGE_SIZE

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

to_date = datetime.utcnow().strftime("%Y-%m-%d")
from_date = (datetime.utcnow() - timedelta(days=TIMEFRAME)).strftime("5Y-%m-%d")
def fetch_news(query="Tesla"):
  url = "https://newsapi.org/v2/everything"
  params = {
    "q": NEWS_QUERY,
    "from": NEWS_FROM_DATE,
    "to": NEWS_TO_DATE,
    "sortBy": "relevancy",
    "language": "en",
    "pageSize": NEWS_PAGE_SIZE,
    "apiKey": NEWS_API_KEY
  }
  response = requests.get(url, params=params)
  data = response.json()

  articles = data.get("articles", [])
  rows = []
  for article in articles:
    rows.append({
      "date": article["publishedAt"],
      "title": article["title"],
      "description": article["description"],
      "url": article["url"],
      "source": article["source"]["name"]
    })
  
  df = pd.DataFrame(rows)
  df.to_csv("data/output/news.csv", index=False)
  print(f"Saved {len(df)} articles to data/output/news.csv")

if __name__ == "__main__":
  fetch_news()
