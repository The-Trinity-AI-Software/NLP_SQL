# data_loader.py
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.dialects.mysql import insert as mysql_insert
from config import MYSQL_CONFIG
import os, sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

def create_sql_engine(database):
    conn_str = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{database}"
    return create_engine(conn_str)

def table_exists(engine, table_name):
    inspector = inspect(engine)
    return inspector.has_table(table_name)

def upload_and_insert_table(filepath, database, table_name):
    ext = filepath.split('.')[-1].lower()
    df = pd.read_csv(filepath) if ext == "csv" else pd.read_excel(filepath)
    engine = create_sql_engine(database)

    with engine.connect() as conn:
        if table_name == "products":
            df = df[["product", "series", "sales_price"]]
            conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
            df.to_sql(table_name, engine, index=False)
            print(f"[✓] Recreated table: {table_name} with {len(df)} records")
            return

        if table_name == "sales_pipeline":
            df = df[["opportunity_id", "sales_agent", "product", "account", "deal_stage", "engage_date", "close_date", "close_value"]]
            conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
            df.to_sql(table_name, engine, index=False)
            print(f"[✓] Recreated table: {table_name} with {len(df)} records")
            return

        if table_name == "data_dictionary":
            df = df[["Table", "Field", "Description"]]
            conn.execute(text(f"DROP TABLE IF EXISTS `{table_name}`"))
            df.columns = ["`Table`", "`Field`", "Description"]  # Escape reserved keywords
            df.to_sql(table_name, engine, index=False)
            print(f"[✓] Recreated table: {table_name} with {len(df)} records")
            return

    if not table_exists(engine, table_name):
        df.to_sql(table_name, engine, index=False)
        print(f"[✓] Created new table: {table_name} with {len(df)} records")
        return

    with engine.connect() as conn:
        try:
            existing = pd.read_sql(f"SELECT `{df.columns[0]}` FROM `{table_name}`", conn)
            existing_keys = set(existing[df.columns[0]].astype(str).tolist())
            new_df = df[~df[df.columns[0]].astype(str).isin(existing_keys)]
        except Exception as e:
            print(f"[!] Could not fetch existing keys: {e}")
            new_df = df

        if not new_df.empty:
            new_df.to_sql(table_name, engine, index=False, if_exists='append')
            print(f"[+] Inserted {len(new_df)} new records into table: {table_name}")
        else:
            print(f"[-] No new records to insert for table: {table_name}")

def upload_and_insert_multiple_files(filepaths, database):
    for path in filepaths:
        table_name = os.path.splitext(os.path.basename(path))[0]
        upload_and_insert_table(path, database, table_name)

def get_table_content(database, table_name, limit=10):
    engine = create_sql_engine(database)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM `{table_name}` LIMIT {limit}"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df