import pandas as pd
from transformers import pipeline
from datetime import datetime

# load cleaned sources
news = pd.read_csv("data/output/news.csv")
reddit = pd.read_csv("data/output/reddit.csv")

# convert date formats
news["date"] = pd.to_datetime(news["date"]).dt.date
reddit["date"] = pd.to_datetime(reddit["created_utc"], unit="s").dt.date

# apply model to text
def analyze_sentiment(texts, model):
  sentiment = pipeline("sentiment-analysis", model=model)
  results = []
  for text in texts:
    try:
      result = sentiment(text[:512])[0] # limit input to 512 tokens
      label = 1 if result["label"] == "POSITIVE" else -1
      score = result["score"] * label
    except Exception:
      score = 0 # in case of error or blank text
    results.append(score)
  return results

# apply to news and reddit titles
news["sentiment"] = analyze_sentiment(news["title"].astype(str), "ProsusAI/finbert")
reddit["sentiment"] = analyze_sentiment(reddit["title"].astype(str), "distilbert-base-uncased-finetuned-sst-2-english")

# aggregate sentiment daily
news_sentiment = news.groupby("date")["sentiment"].mean().reset_index()
news_sentiment.rename(columns={"sentiment": "news_sentiment"}, inplace=True)

reddit_sentiment = reddit.groupby("date")["sentiment"].mean().reset_index()
reddit_sentiment.rename(columns={"sentiment": "reddit_sentiment"}, inplace=True)

# merge with cleaned dataset
df = pd.read_csv("data/output/clean_data.csv")
df["date"] = pd.to_datetime(df["date"]).dt.date
df = df.merge(news_sentiment, on="date", how="left")
df = df.merge(reddit_sentiment, on="date", how="left")

# fill missing sentiment with 0 (neutral)
df[["news_sentiment", "reddit_sentiment"]] = df[["news_sentiment", "reddit_sentiment"]].fillna(0.0)

# save final result
df.to_csv("data/output/with_sentiment.csv", index=False)
print("Sentiment analysis complete")
