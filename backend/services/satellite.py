import requests
from config import FMP_API_KEY, FMP_URL

def fetch_satellite_data(ticker: str):
  url = f"{FMP_URL}/competitors/{ticker}?apikey={FMP_API_KEY}"
  try:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
  except Exception as e:
    print(f"❌ Satellite fetch error for {ticker}: {e}")
    return None

def extract_competitor_insight(data: dict):
  if isinstance(data, dict) and "competitors" in data:
    comps = data["competitors"]
    if comps:
      top_names = [c["name"] for c in comps[:3]]
      return {
        "industry": data.get("industry", "Unknown"),
        "insight": f"Key competitors include: {', '.join(top_names)}",
        "raw_competitors": comps
      }
    else:
      print("⚠️ Competitor list is empty.")
      return {"insight": "No competitors found."}
  else:
    print(f"❌ Unexpected competitor format: {data}")
    return {"insight": "Invalid competitor data format."}
