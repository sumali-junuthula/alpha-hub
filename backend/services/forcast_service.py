from datetime import datetime, timedelta
from models.schema import ForecastResponse, ForecastPoint
import random

def get_mock_forecast(ticker: str) -> ForecastResponse:
    today = datetime.today()
    forecast = []

    for i in range(7):
        date = today + timedelta(days=i)
        predicted_return = round(random.uniform(-2.5, 2.5), 2)
        confidence = round(random.uniform(0.6, 0.95), 2)
        forecast.append(ForecastPoint(
            date=date.strftime("%Y-%m-%d"),
            predicted_return=predicted_return,
            confidence=confidence
        ))

    return ForecastResponse(
        ticker=ticker.upper(),
        forecast=forecast
    )
