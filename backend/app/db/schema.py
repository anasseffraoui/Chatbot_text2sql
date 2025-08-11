from sqlalchemy import text
from functools import lru_cache
from .engine import get_engine

@lru_cache(maxsize=1)
def get_schema_snapshot():
    eng = get_engine()
    sql = """
    SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION;
    """
    rows = []
    with eng.connect() as conn:
        for r in conn.execute(text(sql)):
            rows.append(tuple(r))
    by_table = {}
    for s,t,c,d in rows:
        key = f"{s}.{t}"
        by_table.setdefault(key, []).append((c,d))
    return by_table

def schema_to_prompt(limit_tables=25, limit_cols=40):
    snap = get_schema_snapshot()
    parts = ["Database Engine: SQL Server", "Schema:"]
    i = 0
    for tbl, cols in snap.items():
        if i >= limit_tables: break
        sample = ", ".join(f"{c} ({d})" for c,d in cols[:limit_cols])
        parts.append(f"- {tbl}: {sample}")
        i += 1
    return "\n".join(parts)
