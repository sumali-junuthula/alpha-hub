from fastapi import FastAPI
from api import company, forecast

app = FastAPI(title="AlphaHub API")

app.include_router(company.router)
app.include_router(forecast.router)
