import os
from openai import OpenAI
from dotenv import load_dotenv
from services.signal_fusion import collect_signals
from config import OPENAI_API_KEY

load_dotenv()
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_summary(ticker, signals):
  prompt = f"""
You are a financial analyst. Explain in plain language why the stock price of {ticker} is forecasted to change, based on the following data signals:

{signals}

Your summary should:
- Highlight the most influential signals
- Include confidence if possible
- Be concise and clear
"""
  response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.4,
    max_tokens=300
  )

  return response.choices[0].message.content.strip()

def explain_forecast(ticker):
  # 🚀 Use real collected signals
  signals = collect_signals(ticker)

  summary = generate_summary(ticker, signals)

  return {
    "ticker": ticker,
    "summary": summary,
    "explanations": [
      {"source": k, "weight": 0.25, "summary": v}
      for k, v in signals.items()
    ]
  }
