from ..db.schema import schema_to_prompt
from ..model.prompt import build_prompt
from ..model.client import call_model
from ..db.executor import extract_sql, is_select_only, run_select
from ..utils.errors import bad_request
from .export_service import write_excel

def handle_query(question: str, max_preview_rows: int, show_sql: bool):
    schema_text = schema_to_prompt()
    prompt = build_prompt(schema_text, question, max_rows=max_preview_rows)

    raw = call_model(prompt)
    sql = extract_sql(raw)

    if not is_select_only(sql):
        bad_request("Model produced a non-SELECT or unsafe query.")

    # Execute and normalize
    cols, rows = run_select(sql, preview_limit=max_preview_rows)
    cols = list(cols or [])
    rows = [list(r) for r in (rows or [])]

    # Detect scalar (exactly 1 column and 1 row)
    is_scalar = (len(cols) == 1 and len(rows) == 1)

    # Tabular = anything that is NOT a single-cell scalar
    is_tabular = not is_scalar

    # Only build an Excel download for tabular (multi-row/col) results
    token = None
    if is_tabular and rows:
        _, token = write_excel(cols, rows)

    resp = {
        "sql": sql if show_sql else None,
        "is_tabular": is_tabular,
        # Always return arrays — never null — so the UI can render reliably
        "columns": cols,
        "preview_rows": rows,
        "total_rows": None,          # set if you compute it
        "download_token": token,
        # keep or remove; your UI ignores this now
        "warnings": (["Preview truncated"] if rows and len(rows) >= max_preview_rows else [])
    }

    # Expose scalar value so the UI can show a big single number
    if is_scalar:
        resp["value"] = rows[0][0]

    return resp
