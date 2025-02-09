import mysql.connector
import os
from fastapi import FastAPI
import requests
import socket
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

# Database credentials from environment variables (can be configured in the environment)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

# Account credentials (can be used for creating user accounts or authentication)
ACCOUNT_USER = os.getenv("ACCOUNT_USER", "account_user")
ACCOUNT_PASSWORD = os.getenv("ACCOUNT_PASSWORD", "account_password")

# API URL for the other application (passed dynamically)
API_URL = os.getenv("API_URL", "http://localhost:8000/api3")

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# API 2: Static JSON Response
@app.get("/api2")
def get_static_json():
    return {"message": "This is a static JSON", "status": "success"}

# API 3: Host Name or Pod Name with DateTime (for Application B)
@app.get("/api3")
def get_host_name():
    return {
        "hostname": socket.gethostname(),
        "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# API 4: Sample Insert Value into DB
class Item(BaseModel):
    name: str
    description: str

@app.post("/api4")
def insert_value(item: Item):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (name VARCHAR(255), description TEXT)")
    cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (item.name, item.description))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item inserted successfully", "item": item}

# API 5: Sample Get Value from DB
@app.get("/api5")
def get_value_from_db():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"items": records}

# API 6: Fetch Host Name or Pod Name from another Application (passed API URL)
@app.get("/api6")
def get_other_app_host_info():
    response = requests.get(API_URL)  # Call the other app's API 3 endpoint
    return response.json()
