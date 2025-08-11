import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..services.token_service import verify
from ..config import settings

router = APIRouter(prefix="/download", tags=["download"])

@router.get("/{token}")
def download(token: str):
    payload = verify(token, max_age=settings.DOWNLOAD_TTL_SEC)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
    path = payload.get("path")
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename="results.xlsx")
