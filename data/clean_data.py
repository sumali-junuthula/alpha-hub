import pandas as pd
import numpy as np
from datetime import datetime

# load raw csv files
news = pd.read_csv("data/output/news.csv")
reddit = pd.read_csv("data/output/reddit.csv")
trends = pd.read_csv("data/output/trends.csv")
prices = pd.read_csv("data/output/prices.csv")

# normalize dates
news["date"] = pd.to_datetime(news["date"]).dt.date
reddit["date"] = pd.to_datetime(reddit["created_utc"], unit="s").dt.date

# group by date
news_daily = news.groupby("date").size().reset_index(name="news_count")
reddit_daily = reddit.groupby("date").agg({
  "title": "count",
  "score": "sum",
  "num_comments": "sum"
}).reset_index()
reddit_daily.rename(columns={"title": "reddit_posts"}, inplace=True)

# clean google trends
trends["date"] = pd.to_datetime(trends["date"]).dt.date
trends.rename(columns={trends.columns[2]: "trend_score"}, inplace=True)
trends = trends[["date", "trend_score"]]

# clean price data
prices["date"] = pd.to_datetime(prices["Date"]).dt.date
prices = prices[["date", "Close"]]
prices.rename(columns={"Close": "close_price"}, inplace=True)

# merge all tables
df = prices.copy()
df = df.merge(news_daily, on="date", how="left")
df = df.merge(reddit_daily, on="date", how="left")
df = df.merge(trends, on="date", how="left")

# handle missing data
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(0)

# save final cleaned dataset
df.sort_values("date", inplace=True)
df.to_csv("data/output/clean_data.csv", index=False)
print(f"Saved clean dataset with shape {df.shape} to data/output/clean_date.csv")
