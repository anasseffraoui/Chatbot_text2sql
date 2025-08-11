from dotenv import load_dotenv
import os
load_dotenv()  # loads .env from current working dir

print("DB_DRIVER =", os.getenv("DB_DRIVER"))
print("DB_SERVER =", os.getenv("DB_SERVER"))
print("DB_DATABASE =", os.getenv("DB_DATABASE"))
print("DB_UID =", os.getenv("DB_UID"))
print("HAS_PWD =", bool(os.getenv("DB_PWD")))
