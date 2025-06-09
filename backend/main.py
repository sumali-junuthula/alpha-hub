from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import forecast, reddit, news, google, resolve, competitors, satellite, valuation, deals, earnings, dcf, risks, synergy, heatmap, explainer, sector

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
app.include_router(reddit.router, prefix="/reddit")
app.include_router(news.router, prefix="/news")
app.include_router(google.router, prefix="/google")
app.include_router(resolve.router, prefix="/resolve")
app.include_router(competitors.router, prefix="/competitors")
app.include_router(satellite.router, prefix="/satellite")
app.include_router(valuation.router, prefix="/valuation")
app.include_router(deals.router, prefix="/deals")
app.include_router(earnings.router, prefix="/earnings")
app.include_router(dcf.router, prefix="/dcf")
app.include_router(risks.router, prefix="/risks")
app.include_router(synergy.router, prefix="/synergy")
app.include_router(heatmap.router, prefix="/heatmap")
app.include_router(explainer.router, prefix="/explainer")
app.include_router(sector.router, prefix="/sector")

@app.get("/")
def read_root():
  return {"message": "AlphaHub API is live"}
