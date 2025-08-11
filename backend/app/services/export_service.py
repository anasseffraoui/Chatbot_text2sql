import os, tempfile, pandas as pd
from .token_service import sign
from ..config import settings

def write_excel(columns: list[str], rows: list[list]) -> tuple[str, str]:
    df = pd.DataFrame(rows, columns=columns)
    tmpdir = tempfile.gettempdir()
    path = os.path.join(tmpdir, f"text2sql_export_{os.getpid()}.xlsx")
    df.to_excel(path, index=False)
    token = sign({"path": path})
    return path, token
