import pandas as pd
import joblib
from datetime import datetime

# load today's features
df = pd.read_csv("data/output/features.csv")
latest = df.sort_values("date").iloc[-1]

# load trained model
model = joblib.load("data/output/model.pkl")

# define features columns
features = ["sentiment_3d_avg", "reddit_mentions", "trend_score"]
X = latest[features].values.reshape(1, -1)

# predict class (0 = down/hold, 1 = up/buy)
prediction = model.predict(X)[0]
probability = model.predict_proba(X)[0][1]

# strategy logic
if prediction == 1 and probability > 0.6:
  action = "🟢 BUY - Confidence: {:.1f}%".format(probability * 100)
elif prediction == 1:
  action = "🟡 HOLD - Weak signal to buy"
else:
  action = "🔴 SELL or WAIT - Negative signal"

# output
print("📅 Date:", latest["date"])
print("📊 Features:", dict(zip(features, X[0])))
print("🤖 Model prediction:", prediction)
print("📈 Strategy Recommendation:", action)
