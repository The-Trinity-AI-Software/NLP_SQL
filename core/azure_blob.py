from azure.storage.blob import BlobServiceClient
from config import AZURE_BLOB_CONFIG
import os, sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

def upload_to_blob(local_path, blob_name):
    blob_service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONFIG["connection_string"])
    container = blob_service.get_container_client(AZURE_BLOB_CONFIG["container_name"])
    with open(local_path, "rb") as data:
        container.upload_blob(name=blob_name, data=data, overwrite=True)
