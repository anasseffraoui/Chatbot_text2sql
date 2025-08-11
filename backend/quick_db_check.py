# quick_db_check.py
import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

server  = os.getenv("DB_SERVER")
db      = os.getenv("DB_DATABASE")
uid     = os.getenv("DB_UID")
pwd     = os.getenv("DB_PWD")

# Try these in order; the script skips those not installed
candidates = [
    os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
    "ODBC Driver 18 for SQL Server",
    "ODBC Driver 17 for SQL Server",
]

print("Installed ODBC drivers:", pyodbc.drivers())

for drv in candidates:
    if drv not in pyodbc.drivers():
        print(f"\nSkipping {drv} (not installed)")
        continue

    # NOTE the double braces around {drv} — required by ODBC connection strings
    conn = (
        f"DRIVER={{{drv}}};"
        f"SERVER={server};"
        f"DATABASE={db};"
        f"UID={uid};PWD={pwd};"
        f"Encrypt=yes;TrustServerCertificate=yes;"
    )
    print(f"\nTrying driver: {drv}")
    try:
        cn = pyodbc.connect(conn, timeout=5)
        cur = cn.cursor()
        cur.execute("SELECT 1")
        print("✅ Connected OK with", drv)
        break
    except Exception as e:
        print(f"❌ {drv} failed: {e}")
