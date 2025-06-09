from .valuation import get_comps_by_industry, get_ratios

def get_positioning_heatmap(ticker, industry):
  comps = get_comps_by_industry(industry, exclude_ticker=ticker)

  metrics = ["priceEarningsRatioTTM", "evToEbitdaTTM", "evToSalesTTM", "netProfitMarginTTM", "revenueGrowthTTM"]
  metric_labels = {
    "priceEarningsRatioTTM": "P/E",
    "evToEbitdaTTM": "EV/EBITDA",
    "evToSalesTTM": "EV/Sales",
    "netProfitMarginTTM": "Profit Margin",
    "revenueGrowthTTM": "Revenue Growth"
  }

  heatmap = []

  for metric in metrics:
    row = {"metric": metric_labels[metric], "peers": []}
    for comp in comps:
      try:
        ratios = get_ratios(comp["symbol"])
        row["peers"].append({
          "ticker": comp["symbol"],
          "value": float(ratios.get(metric, 0))
        })
      except:
        continue
    heatmap.append(row)

  return heatmap
