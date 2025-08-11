from fastapi import HTTPException

def bad_request(msg: str):
    raise HTTPException(status_code=400, detail=msg)

def server_error(msg: str):
    raise HTTPException(status_code=500, detail=msg)
