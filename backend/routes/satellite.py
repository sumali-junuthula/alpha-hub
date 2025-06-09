from fastapi import APIRouter, Query
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/")
def get_satellite_signal(ticker: str = Query(..., min_length=1)):
  base_date = datetime.today()
  days = [base_date - timedelta(days=i) for i in range(10)]
  dates = [d.strftime("%Y-%m-%d") for d in reversed(days)]

  # Simulated proxy data (e.g., parking lot traffic index 0-100)
  mock_activity = [50, 52, 55, 58, 53, 60, 65, 70, 68, 75]

  return {
    "ticker": ticker.upper(),
    "signal": mock_activity,
    "dates": dates,
    "metric": "Estimated Location Activity"
  }
