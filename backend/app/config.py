from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    ENV: str = os.getenv("ENV", "dev")

    FEATHERLESS_URL: str = os.getenv("FEATHERLESS_URL", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    HF_MODEL: str = os.getenv("HF_MODEL", "")

    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
    DB_DATABASE: str = os.getenv("DB_DATABASE", "")
    DB_UID: str = os.getenv("DB_UID", "")
    DB_PWD: str = os.getenv("DB_PWD", "")

    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5500")
    MAX_PREVIEW_ROWS: int = int(os.getenv("MAX_PREVIEW_ROWS", "50"))
    DOWNLOAD_TTL_SEC: int = int(os.getenv("DOWNLOAD_TTL_SEC", "600"))
    HMAC_SECRET: str = os.getenv("HMAC_SECRET", "dev-secret-change-me")

settings = Settings()
