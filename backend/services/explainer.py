import os
import openai
from dotenv import load_dotenv
from config import OPENAI_API_KEY

load_dotenv()

def generate_summary(ticker, signals):
  prompt = f"""
You are a financial analyst. Explain in plain language why the stock price of {ticker} is forecasted to change, based on the following data signals:

{signals}

Your summary should:
- Highlight the most influential signals
- Include confidence if possible
- Be concise and clear
"""
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.4,
    max_tokens=300
  )

  return response['choices'][0]['message']['content'].strip()


def explain_forecast(ticker: str):
  # Replace this with dynamic signal fetching later
  signals = {
    "Reddit": "Spike in mentions (120%) — bullish sentiment",
    "News": "Positive sentiment (0.74) — Apple beats earnings",
    "Google": "Surge in search volume last 7 days",
    "Competitor": "Samsung delays launch — favorable for Apple"
  }

  summary = generate_summary(ticker, signals)

  return {
    "ticker": ticker,
    "summary": summary,
    "explanations": [
      {"source": k, "weight": 0.25, "summary": v}
      for k, v in signals.items()
    ]
  }
