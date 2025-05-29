import pandas as pd
import joblib

# load data and mondel
df = pd.read_csv("data/output/features.csv")
model = joblib.load("data/output/model.pkl")

# select features and target
features = ["sentiment_3d_avg", "reddit_mentions", "trend_score"]
df["predicted"] = model.predict(df[features])
df["actual"] = df["price_change_3d"].apply(lambda x: 1 if x > 0 else 0)

# simulate strategy: buy if predicted == 1
df["strategy_return"] = df.apply(
  lambda row: row["price_change_3d"] if row["predicted"] == 1 else 0,
  axis=1
)

# calculate stats
accuracy = (df["predicted"] == df["actual"]).mean()
total_return = df["strategy_return"].sum()

print(f"📈 Model accuracy: {accuracy:.2%}")
print(f"💰 Simulated strategy return: {total_return:.2f}% over {len(df)} days")
