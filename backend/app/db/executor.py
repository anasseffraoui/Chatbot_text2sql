import re
from sqlalchemy import text
from .engine import get_engine

FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|TRUNCATE|CREATE|EXEC|EXECUTE|GRANT|REVOKE|DENY|BACKUP|RESTORE|DECLARE|BEGIN\s+TRAN|COMMIT|ROLLBACK|BULK|OPENROWSET|OPENDATASOURCE|XP_CMDSHELL)\b",
    re.IGNORECASE
)

def extract_sql(raw: str) -> str:
    s = raw.strip()
    s = re.sub(r"^```sql|^```|```$", "", s, flags=re.IGNORECASE|re.MULTILINE).strip()
    s = s.split(";")[0].strip()
    return s

def is_select_only(sql: str) -> bool:
    if FORBIDDEN.search(sql):
        return False
    return re.match(r"^\s*SELECT\b", sql, re.IGNORECASE) is not None

def force_top(sql: str, top_n: int = 1000) -> str:
    if re.match(r"^\s*SELECT\s+TOP\s+\d+", sql, re.IGNORECASE):
        return sql
    if re.search(r"\bOFFSET\s+\d+\s+ROWS\b", sql, re.IGNORECASE):
        return sql
    return re.sub(r"^\s*SELECT\b", f"SELECT TOP {top_n}", sql, flags=re.IGNORECASE)

def run_select(sql: str, preview_limit: int = 50, timeout_sec: int = 15):
    eng = get_engine()
    capped = force_top(sql, max(preview_limit, 100))
    rows, cols = [], []
    with eng.connect() as conn:
        conn.exec_driver_sql(f"SET LOCK_TIMEOUT {timeout_sec*1000}")
        res = conn.execute(text(capped))
        cols = [c for c in res.keys()]
        for i, row in enumerate(res):
            if i < preview_limit:
                rows.append(list(row))
    return cols, rows
