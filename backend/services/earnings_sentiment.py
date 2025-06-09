import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import KEYWORDS_POSITIVE, KEYWORDS_NEGATIVE, NEWS_API_KEY

load_dotenv()

def mock_sentiment_score(text):
  text_lower = text.lower()
  score = 0
  for word in KEYWORDS_POSITIVE:
    if word in text_lower:
      score += 1
  for word in KEYWORDS_NEGATIVE:
    if word in text_lower:
      score -= 1
  if score > 0:
    return "positive"
  elif score < 0:
    return "negative"
  else:
    return "neutral"

def analyze_earnings_sentiment(ticker):
  query = f"{ticker} earnings"
  to_date = datetime.now().strftime("%Y-%m-%d")
  from_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")

  url = "https://newsapi.org/v2/everything"
  params = {
    "q": query,
    "from": from_date,
    "to": to_date,
    "language": "en",
    "sortBy": "relevancy",
    "pageSize": 10,
    "apiKey": NEWS_API_KEY
  }

  try:
    res = requests.get(url, params=params)
    res.raise_for_status()
    articles = res.json().get("articles", [])

    results = []
    sentiment_count = {"positive": 0, "negative": 0, "neutral": 0}

    for article in articles:
      title = article["title"]
      sentiment = mock_sentiment_score(title)
      sentiment_count[sentiment] += 1
      results.append({"title": title, "sentiment": sentiment})

    # Aggregate
    dominant_sentiment = max(sentiment_count, key=sentiment_count.get)
    confidence = sentiment_count[dominant_sentiment] / max(1, sum(sentiment_count.values()))

    return {
      "ticker": ticker.upper(),
      "summary_sentiment": dominant_sentiment,
      "confidence": round(confidence, 2),
      "headlines": results
    }

  except Exception as e:
    raise RuntimeError(f"Earnings sentiment fetch error: {e}")
