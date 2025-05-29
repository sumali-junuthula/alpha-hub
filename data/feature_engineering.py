import pandas as pd

df = pd.read_csv("data/output/with_sentiment.csv")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df["data"] = pd.to_datetime(df["date"])

df["sentiment_3d_avg"] = df["news_sentiment"].rolling(window=3).mean()
df["reddit_mentions"] = df["reddit_posts"]
df["trend_score"] = df["trend_score"]
df["trend_score"] = df["trend_score"] / 100

# formula = [(P(today) - P(3 days ago)) / P(3 days ago)] * 100
df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")
df["close_price"] = df["close_price"].ffill()
df["price_change_3d"] = df["close_price"].pct_change(periods=3) * 100

# drop rows with missing values
df.dropna(inplace=True)

# save final feature-ready dataset
df.to_csv("data/output/features.csv", index=False)
print(f"Saved engineered features to data/output/features.csv with shape {df.shape}")
