# 🔮 AlphaHub

**AI-Powered, Signal-Rich Stock Forecasting Platform**  
*Future-facing forecasts. Signal-level insights. Built for quants.*

---

## 🧠 What is AlphaHub?

AlphaHub is an advanced stock price forecasting platform that uses **multi-modal data** — Reddit sentiment, Google Trends, news headlines, competitor movements, and even satellite imagery — to generate accurate, explainable stock predictions over 7, 30, and 90-day horizons.

It’s Bloomberg Terminal meets GPT-powered analytics — built to stand out in quant, hedge fund, and fintech recruiting pipelines.

---

## 🎯 Key Features

| Feature                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| 🔍 Company Search         | Search by company name or ticker.                                           |
| 📈 Forecast Visualization | View 7/30/90-day price forecasts with confidence bands.                    |
| 🧠 Signal Dashboard       | Track Reddit mentions, sentiment scores, news spikes, and Google Trends.   |
| 🔗 Competitor Analytics   | Analyze how peer companies impact the forecast.                            |
| 📊 Explainable AI         | Understand the top features that drove the prediction.                     |
| 🛰️ Satellite Integration  | (Optional) Visual activity scores from factory imagery.                    |
| 💾 Export & API Access    | Download forecasts, connect via API, and run backtests.                    |

---

## 📦 Tech Stack

| Layer                | Tools & Libraries                             |
|----------------------|-----------------------------------------------|
| Frontend (UI)        | React.js (Next.js), TailwindCSS, Chart.js     |
| Backend (API)        | FastAPI, Uvicorn, CORS, yfinance              |
| ML/AI                | PyTorch, scikit-learn, LSTM / Transformer     |
| NLP/Sentiment        | HuggingFace Transformers (`finBERT`, `T5`)    |
| Data Pipelines       | Reddit (PRAW), Google Trends (pytrends), NewsAPI |
| Database             | PostgreSQL, Redis, or SQLite for MVP          |
| Cloud (optional)     | Render, Vercel, S3, Railway, or GCP           |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/AlphaHub.git
cd AlphaHub
