import sqlite3
import pickle
import os
from flask import Flask, request

app = Flask(__name__)

SECRET_KEY = "hardcoded-secret-abc123"
DB_PASSWORD = "admin123"

@app.route("/login", methods=["POST"])
def login():
username = request.form.get("username")
password = request.form.get("password")
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute(query)
return str(cursor.fetchall())

@app.route("/deserialize", methods=["POST"])
def deserialize():
data = request.get_data()
obj = pickle.loads(data)
return str(obj)

@app.route("/ping", methods=["GET"])
def ping():
host = request.args.get("host", "127.0.0.1")
result = os.popen(f"ping -c 1 {host}").read()
return result

if name == "__main__":
app.run(debug=True)
