# database_utils.py
import pymysql
from core.data_loader import create_sql_engine
from config import MYSQL_CONFIG
from sqlalchemy import text
import os, sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

def get_all_databases():
    cfg = MYSQL_CONFIG
    conn = pymysql.connect(
        host=cfg["host"],
        user=cfg["user"],
        password=cfg["password"],
        port=cfg["port"]
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return dbs

def get_all_tables(database):
    engine = create_sql_engine(database)
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = '{database}' AND table_type = 'BASE TABLE';
        """))
        return [row[0] for row in result]
    
def get_columns_for_table(database, table):
    engine = create_sql_engine(database)
    with engine.connect() as conn:
        result = conn.execute(text(f"SHOW COLUMNS FROM `{table}`;"))
        return [row[0] for row in result]
    
def get_recent_records(database, table):
    engine = create_sql_engine(database)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM `{table}` ORDER BY 1 DESC LIMIT 10"))
        columns = result.keys()
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
    return rows

