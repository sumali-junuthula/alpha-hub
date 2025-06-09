from fastapi import APIRouter, Query, HTTPException
from services.synergy import estimate_synergy_deal

router = APIRouter()

@router.get("/")
def simulate_synergy(
  target_revenue: float = Query(..., description="Target company revenue in USD"),
  target_margin: float = Query(..., description="Target operating margin as decimal"),
  expected_synergies: float = Query(..., description="Expected synergy value in USD"),
  deal_cost: float = Query(..., description="Cost of deal in USD")
):
  try:
    result = estimate_synergy_deal(target_revenue, target_margin, expected_synergies, deal_cost)
    return result
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
