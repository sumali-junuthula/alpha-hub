# 🧠 AlphaHub: A Real-Time Multi-Modal Alpha Signal Engine

AlphaHub is a full-stack, real-time alpha discovery platform that collects and fuses **alternative data sources** — including news headlines, Reddit sentiment, Google Trends, and satellite imagery — to generate actionable **trading signals** using **reinforcement learning** and **quantitative modeling**.

The project simulates a signal research desk at a modern hedge fund, combining state-of-the-art AI techniques with rigorous financial engineering to dynamically adapt to changing market conditions.

---

## 🚀 Key Features

- **Multi-Source Data Ingestion**:
  - 🗞️ Real-time news headlines (via NewsAPI)
  - 🧵 Reddit mentions and sentiment (via Pushshift or PRAW)
  - 📈 Google Trends (via PyTrends)
  - 🛰️ Satellite and visual data (optional via CLIP/ViT)

- **Signal Generation**:
  - Transformer-based NLP for sentiment extraction
  - Trend-based anomaly detection from public interest
  - Price-based technical indicators for baseline modeling
  - Optional visual signal processing with CLIP for product activity estimation

- **Alpha Modeling Engine**:
  - Reinforcement learning (PPO) agent allocates capital dynamically based on signal vector
  - Environment simulates realistic trading conditions with slippage and execution lag

- **Backtesting Framework**:
  - Portfolio simulation with Sharpe, drawdown, IC, turnover, and PnL metrics
  - Benchmarks include momentum, mean-reversion, and equal-weight strategies

- **Explainable Intelligence**:
  - Model introspection and signal attribution
  - Optional natural language explanations via GPT

- **Streamlit Dashboard** *(in progress)*:
  - Interactive signal visualizations
  - Equity curve, live allocation weights, news & Reddit sentiment feeds

---

## 📦 Technologies Used

AlphaHub leverages modern data and machine learning tools to collect signals, analyze sentiment, and predict stock movement.

### 🧹 Data Collection
- **requests** – Pulls data from news, Reddit, and Google Trends APIs
- **pandas**, **datetime** – Cleans and processes time-series data
- **dotenv** – Manages API keys securely

### 🔍 Sentiment Analysis
- **transformers**, **torch** – Uses DistilBERT for classifying sentiment from text
- **pipeline("sentiment-analysis")** – Runs pre-trained NLP models on news and Reddit posts

### 📊 Feature Engineering
- **pandas**, **numpy** – Creates features like 3-day sentiment averages, trend scores, and price % change

### 🧠 Machine Learning
- **scikit-learn** – Trains a RandomForestClassifier to predict price direction
- **train_test_split**, **classification_report**, **joblib** – For evaluation and model saving

### ⚙️ System & Deployment
- **venv**, **VS Code** – Development and environment setup
- *(Optional)* **Flask**, **Streamlit**, or **Docker** – For deploying the prediction engine or dashboard

---

## 🧠 Why AlphaHub?

> AlphaHub is designed to push the boundary of what undergraduates can build — applying cutting-edge machine learning and autonomous agent frameworks to real-world financial data. The project replicates the **quantitative signal discovery process used at Citadel, Point72, and Renaissance Technologies**, making it a powerful portfolio piece for internships and research roles.

---

## 🗂️ Repository Structure

```bash
alphahub/
├── data/            # Raw + processed data
├── signals/         # Scripts for generating signals from various sources
├── models/          # NLP models and signal transformers
├── rl_agents/       # Reinforcement learning environment and training scripts
├── backtests/       # Portfolio simulation, evaluation metrics
├── dashboard/       # Streamlit frontend (in progress)
├── research/        # Whitepapers, diagrams, and documentation
├── utils/           # Common utilities and data loaders
├── main.py          # Pipeline entry point
└── requirements.txt
