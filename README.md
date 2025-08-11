# CHU Text2SQL

FastAPI backend that converts NL questions to SQL, executes them via pyodbc, and returns a preview + Excel download.
Single-file HTML UI included.

## Run locally

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
