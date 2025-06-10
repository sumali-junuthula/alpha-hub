import requests

BASE_URL = "http://0.0.0.0:10000"

def fetch_signal(endpoint, ticker):
  try:
    res = requests.get(f"{BASE_URL}/{endpoint}/?ticker={ticker}")
    res.raise_for_status()
    return res.json()
  except Exception as e:
    print(f"Failed to fetch {endpoint} for {ticker}: {e}")
    return None

def collect_signals(ticker):
  reddit = fetch_signal("reddit", ticker)
  news = fetch_signal("news", ticker)
  google = fetch_signal("google", ticker)
  competitor = fetch_signal("competitors", ticker)

  signals = {}

  # ✅ Reddit: list of posts — summarize manually
  if reddit and isinstance(reddit, list):
    titles = [r["title"] for r in reddit[:3]]
    signals["Reddit"] = f"Top mentions: {'; '.join(titles)}"

  # ✅ News: list of articles — summarize manually
  if news and isinstance(news, list):
    summaries = [f"{a['title']}" for a in news[:3]]
    signals["News"] = f"Recent headlines: {'; '.join(summaries)}"

  # ✅ Google: trend array — extract last few days or average
  if google and isinstance(google, dict) and "interest" in google:
    last_trend = google["interest"][-3:]
    avg = sum(last_trend) / len(last_trend)
    signals["Google"] = f"Avg trend score over last 3 days: {round(avg)}"

  if isinstance(competitor, dict) and "competitors" in competitor:
    comps = competitor["competitors"]
    if comps:
      top_names = [c["name"] for c in comps[:3]]  # take top 3 competitors
      signals["Competitor"] = f"Key competitors include: {', '.join(top_names)}"
    else:
      print("⚠️ Competitor list is empty.")
  else:
    print(f"❌ Unexpected competitor data format: {competitor}")

  return signals
