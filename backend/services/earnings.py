import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from config import GNEWS_LOOKBACK_DAYS, GNEWS_API_KEY, KEYWORDS_POSITIVE, KEYWORDS_NEGATIVE

load_dotenv()

def mock_sentiment_score(text):
  text = text.lower()
  score = 0
  for word in KEYWORDS_POSITIVE:
    if word in text:
      score += 1
  for word in KEYWORDS_NEGATIVE:
    if word in text:
      score -= 1
  if score > 0:
    return "positive"
  elif score < 0:
    return "negative"
  return "neutral"

def analyze_earnings_sentiment(ticker: str):
  if not GNEWS_API_KEY:
    raise RuntimeError("GNEWS_API_KEY is missing in environment")

  url = "https://gnews.io/api/v4/search"
  to_date = datetime.now().strftime("%Y-%m-%d")
  from_date = (datetime.now() - timedelta(days=GNEWS_LOOKBACK_DAYS)).strftime("%Y-%m-%d")

  params = {
    "q": f"{ticker} earnings",
    "lang": "en",
    "from": from_date,
    "to": to_date,
    "max": 10,
    "token": GNEWS_API_KEY
  }

  try:
    res = requests.get(url, params=params)
    res.raise_for_status()
    articles = res.json().get("articles", [])

    sentiment_count = {"positive": 0, "negative": 0, "neutral": 0}
    results = []

    for article in articles:
      title = article.get("title", "")
      if "earnings" not in title.lower():
        continue

      sentiment = mock_sentiment_score(title)
      sentiment_count[sentiment] += 1
      results.append({
        "title": title,
        "url": article.get("url", ""),
        "sentiment": sentiment
      })

    if not results:
      return {
        "ticker": ticker.upper(),
        "summary_sentiment": "neutral",
        "confidence": 0.0,
        "headlines": []
      }

    dominant = max(sentiment_count, key=sentiment_count.get)
    confidence = sentiment_count[dominant] / sum(sentiment_count.values())

    return {
      "ticker": ticker.upper(),
      "summary_sentiment": dominant,
      "confidence": round(confidence, 2),
      "headlines": results
    }

  except Exception as e:
    raise RuntimeError(f"GNews earnings sentiment error: {e}")
