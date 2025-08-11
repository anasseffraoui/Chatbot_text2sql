from fastapi import APIRouter
from sqlalchemy import text
from ..db.engine import get_engine

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health():
    db_ok = False
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return {"status":"ok", "db":"ok" if db_ok else "down"}
