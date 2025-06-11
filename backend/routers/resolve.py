from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/")
def resolve_echo(query = Query(...):
  return {"resolved": query}
