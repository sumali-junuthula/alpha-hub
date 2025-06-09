from fastapi import APIRouter, Query, HTTPException
from services.sector import get_sector_commentary

router = APIRouter()

@router.get("/")
def fetch_sector_commentary(sector: str = Query(..., description="Name of the sector to analyze")):
  try:
    return get_sector_commentary(sector)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
