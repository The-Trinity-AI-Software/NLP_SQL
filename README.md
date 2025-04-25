# 🧠 NLP-to-SQL Dashboard (CRM Data Explorer)

This project is a powerful and interactive web dashboard that allows users to upload structured data (CSV/XLSX), explore existing MySQL tables, and query the data using **natural language** — which is automatically translated into SQL.

---

## 🚀 Features

- ✅ Upload CSV/XLSX files into MySQL as structured tables
- ✅ Works with multiple databases — dynamically fetch tables and columns
- ✅ NLP Query Input → SQL Translation using local LLM (`sqlcoder`, `codellama`, etc.)
- ✅ Automatically preview recent records and columns per table
- ✅ Conditional file upload: only when needed
- ✅ Responsive, clean UI with professional UX

---

## 📁 Folder Structure

```
├── app.py                # Flask backend
├── config.py             # MySQL connection settings
├── templates/
│   └── index.html        # Full dashboard UI
├── core/
│   ├── data_loader.py    # File upload + table insert logic
│   ├── database_utils.py # Table listing and metadata fetch
│   └── sql_pipeline.py   # NLP-to-SQL logic with LLM
├── uploads/              # Uploaded files
└── requirements.txt      # All dependencies
```

---

## 🧑‍💻 How to Use

1. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   python app.py
   ```

3. **Access the dashboard**
   Go to [http://localhost:5000](http://localhost:5000)

4. **Select database** → Choose whether to upload new data  
   OR directly view tables & ask natural language queries.

---

## 💡 Sample NLP Queries

```
Show all accounts and their revenue.
List accounts established after 2010.
Show products priced above 1000.
Find deals closed after 2023.
List all fields in the accounts table.
```

---

## 📦 Models Supported

- `defog/sqlcoder-7b-2` (default, runs locally)
- `codellama/CodeLlama-7b-Instruct`
- `Salesforce/codet5p-220m`
- LLMs integrated using HuggingFace `transformers`

---

## 🛠 Requirements

- Python 3.8+
- MySQL 8.0+ (Ensure running locally or via Docker)
- Transformers (HuggingFace), Flask, Pandas, SQLAlchemy

---

## ✨ Credits

Built with ❤️ for intelligent business querying, CRM data insights, and enterprise-ready SQL automation.

---

For any issues or suggestions, please contact `your_team@company.com`.