# config.py
import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# ✅ MySQL configuration for CRM database
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "port": 3306
}

# ✅ Azure Blob configuration (if needed for uploads)
AZURE_BLOB_CONFIG = {
    "connection_string": "your_azure_blob_connection_string",
    "container_name": "your_container_name"
}
