from fastapi import APIRouter, HTTPException
from models.schema import CompanyInfo
from services.company_service import get_company_data

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("/", response_model=CompanyInfo)
def company_info(ticker: str):
    try:
        return get_company_data(ticker)
    except Exception:
        raise HTTPException(status_code=404, detail="Ticker not found or data fetch failed.")
