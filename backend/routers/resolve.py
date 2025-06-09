from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/")
def resolve_echo(query: str = Query(..., description="Company name or ticker")):
  return {"resolved": query}
