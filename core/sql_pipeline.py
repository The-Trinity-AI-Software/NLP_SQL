from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from core.data_loader import create_sql_engine
import pandas as pd
from core.system_prompt import SYSTEM_PROMPT

# Load once globally
tokenizer = AutoTokenizer.from_pretrained("defog/sqlcoder-7b-2")
model = AutoModelForCausalLM.from_pretrained(
    "defog/sqlcoder-7b-2",
    device_map="auto",
    torch_dtype=torch.float16
)

def generate_prompt(nl_query, tables_schema_dict):
    schema_lines = [f"# Table: {tbl}({', '.join(cols)})" for tbl, cols in tables_schema_dict.items()]
    schema_info = "\\n".join(schema_lines)

    return f"""{SYSTEM_PROMPT}

 ### Database Schema:
 {schema_info}

 ### User Question:
 {nl_query.strip()}

 ### SQL Query:
 SELECT""".strip()

def run_nl_to_sql_pipeline(prompt, db):
    engine = create_sql_engine(db)

    # Tokenize and generate SQL using the prompt
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256, do_sample=False)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Clean up: Ensure SQL starts with SELECT
    if "SELECT" in sql.upper():
        sql = "SELECT" + sql.split("SELECT", 1)[-1]

    try:
        result_df = pd.read_sql(sql, engine)
    except Exception as e:
        result_df = f"SQL Execution Error: {e}"

    return sql.strip(), result_df