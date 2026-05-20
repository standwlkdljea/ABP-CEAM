import mysql.connector

DB_CONFIG = {
    "host": "172.17.30.35",   # IP de la otra máquina
    "port": 3306,
    "user": "compañero",
    "password": "contraseña123",
    "database": "tests"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)