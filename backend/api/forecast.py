from fastapi import APIRouter
from models.schema import ForecastResponse
from services.forecast_service import get_mock_forecast

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("/", response_model=ForecastResponse)
def forecast(ticker: str):
    return get_mock_forecast(ticker)
