import os, urllib
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from ..config import settings

def get_engine() -> Engine:
    conn_str = (
        f"DRIVER={settings.DB_DRIVER};SERVER={settings.DB_SERVER};DATABASE={settings.DB_DATABASE};"
        f"UID={settings.DB_UID};PWD={settings.DB_PWD};TrustServerCertificate=yes;"
    )
    params = urllib.parse.quote_plus(conn_str)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", pool_pre_ping=True)
    # sanity ping
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return engine
