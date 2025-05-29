import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# load cleaned + feature-engineered data
df = pd.read_csv("data/output/features.csv")

# create the target label: 1 if price went up in 3 days, else 0
df["target"] = df["price_change_3d"].apply(lambda x: 1 if x > 0 else 0)

# define the input features your model should use
features = ["sentiment_3d_avg", "reddit_mentions", "trend_score"]
X = df[features]
y = df["target"]

# split data: 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=0.2, random_state=42
)

# train a Random Forest model (like many decision trees working together)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# evaluate the model on the test data
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("✅ Model accuracy on test data:", f"{acc:.2%}")
print("\n🧾 Classification report:\n", classification_report(y_test, y_pred))

# save model to disk for later use in predictions
joblib.dump(model, "data/output/model.pkl")
print("💾 Model saved to data/output/model.pkl")
