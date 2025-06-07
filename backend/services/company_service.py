import yfinance as yf
from models.schema import CompanyInfo, PricePoint

def get_company_data(ticker: str) -> CompanyInfo:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="30d")

    price_history = [
        PricePoint(date=str(idx.date()), close=row["Close"])
        for idx, row in hist.iterrows()
    ]

    return CompanyInfo(
        ticker=ticker.upper(),
        name=info.get("shortName", "N/A"),
        sector=info.get("sector", "N/A"),
        industry=info.get("industry", "N/A"),
        description=info.get("longBusinessSummary", "N/A"),
        price_history=price_history,
    )
