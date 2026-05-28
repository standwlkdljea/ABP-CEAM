import os
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-vet-2026"
    # Database credentials – adjust encoding if needed
    DB_USER = quote_plus("compañero")
    DB_PASS = quote_plus("contrasena123")
    DB_HOST = "172.17.30.35"
    DB_PORT = 3306
    DB_NAME = "vetcuidado_db"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
