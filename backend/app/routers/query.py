from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..services.query_service import handle_query

router = APIRouter(prefix="/query", tags=["query"])

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=4, max_length=1000)
    max_preview_rows: int = 50
    show_sql: bool = True

@router.post("")
def query(req: QueryRequest):
    try:
        return handle_query(req.question, req.max_preview_rows, req.show_sql)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
