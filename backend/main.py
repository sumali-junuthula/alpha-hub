from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import forecast

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
# app.include_router(company.router, prefix="/company", tags=["company"])
# app.include_router(signals.router, prefix="/signals", tags=["signals"])
# app.include_router(strategy.router, prefix="/strategy", tags=["strategy"])

@app.get("/")
def read_root():
  return {"message": "AlphaHub API is live"}
