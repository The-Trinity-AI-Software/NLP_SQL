from core.sql_pipeline import generate_prompt
from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database_utils import get_all_databases, get_all_tables, get_columns_for_table, get_recent_records
from core.sql_pipeline import run_nl_to_sql_pipeline
from core.data_loader import upload_and_insert_table, upload_and_insert_multiple_files
from core.data_loader import create_sql_engine
import pandas as pd
import os, sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    databases = get_all_databases()
    return render_template("index.html", databases=databases)

@app.route("/upload_files", methods=["POST"])
def upload_files():
    selected_db = request.form.get("database")
    uploaded_files = request.files.getlist("file")
    filepaths = []

    for file in uploaded_files:
        if file.filename:
            filename = file.filename
            ext = filename.split(".")[-1].lower()
            if ext in ["csv", "xlsx"]:
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                filepaths.append(filepath)

    if filepaths and selected_db:
        for path in filepaths:
            table_name = os.path.splitext(os.path.basename(path))[0]
            upload_and_insert_table(path, selected_db, table_name)

    return ("", 204)




@app.route("/get_tables", methods=["GET"])
def get_tables():
    db = request.args.get("db")
    if db:
        print(f"⚙️ Fetching tables for selected DB: {db}")
        tables = get_all_tables(db)
        print("✅ Tables found:", tables)
        return jsonify(tables)
    return jsonify([])



@app.route("/get_columns", methods=["GET"])
def get_columns():
    db = request.args.get("db")
    table = request.args.get("table")
    if db and table:
        columns = get_columns_for_table(db, table)
        return jsonify(columns)
    return jsonify([])

@app.route("/get_recent_records", methods=["GET"])
def get_recent_records_route():
    db = request.args.get("db")
    table = request.args.get("table")
    if db and table:
        try:
            records = get_recent_records(db, table)
            return jsonify(records)
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify([])



@app.route("/run_query", methods=["POST"])
def run_query():
    db = request.form.get("database")
    nl_query = request.form.get("query")

    if db and nl_query:
        try:
            tables = get_all_tables(db)
            engine = create_sql_engine(db)

            tables_schema = {}
            for table in tables:
                df = pd.read_sql(f"SELECT * FROM `{table}` LIMIT 1", engine)
                tables_schema[table] = list(df.columns)

            prompt = generate_prompt(nl_query, tables_schema)
            sql, result_df = run_nl_to_sql_pipeline(prompt, db)

            result = result_df.to_string(index=False) if not isinstance(result_df, str) else result_df
            return jsonify({"sql": sql, "result": result})

        except Exception as e:
            return jsonify({"sql": "", "result": f"❌ Error: {str(e)}"})

    return jsonify({"sql": "", "result": "❌ No query or database selected."})


@app.route("/reset", methods=["GET"])
def reset():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
