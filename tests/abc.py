import os
import pickle
import yaml
import hashlib
import sqlite3
import requests
import traceback
import logging
from flask import Flask, request

app = Flask(__name__)

# ============================================================
# A01:2021 - Broken Access Control (IDOR)
# ============================================================
@app.route("/user/<user_id>")
def get_user(user_id):
    # No authentication or authorization check
    return f"Returning data for user {user_id}"

@app.route("/admin/data")
def get_admin_data():
    user_id = request.args.get("id")
    # ❌ directly exposing DB result without auth
    return db.execute(f"SELECT * FROM users WHERE id={user_id}")



# ============================================================
# A02:2021 - Cryptographic Failures
# ============================================================
SECRET_KEY = "secret"   # Hardcoded weak secret key

def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # Weak hash (MD5)


# ============================================================
# A03:2021 - Injection (SQL Injection)
# ============================================================
def sql_injection_example(user_input):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Vulnerable: string concatenation in SQL
    cursor.execute("SELECT * FROM users WHERE name = '" + user_input + "';")
    return cursor.fetchall()


# ============================================================
# A04:2021 - Insecure Design (No CSRF Protection)
# ============================================================
@app.route("/transfer", methods=["POST"])
def transfer_money():
    # No CSRF protection
    amount = request.form.get("amount")
    return f"Transferred {amount}!"


# ============================================================
# A05:2021 - Security Misconfiguration
# ============================================================
app.config["DEBUG"] = True  # Debug enabled in production

@app.route("/cors")
def misconfigured_cors():
    # Permissive CORS (example placeholder)
    return "CORS allows *"


# ============================================================
# A06:2021 - Vulnerable/Outdated Components
# ============================================================
import urllib.request  # Outdated/insecure library usage


# ============================================================
# A07:2021 - Identification & Authentication Failures
# ============================================================
def weak_password_storage():
    password = input("Enter password: ")
    # Password stored in plain text (no hashing)
    with open("pw.txt", "w") as f:
        f.write(password)


def jwt_insecure():
    # Simulating insecure JWT verification
    token = request.args.get("token")
    # Signature verification disabled
    verified = True  # BAD: no validation
    return f"Token accepted: {token}"


# ============================================================
# A08:2021 - Insecure Deserialization
# ============================================================
def insecure_deserialization(data):
    obj = pickle.loads(data)  # Vulnerable
    return obj

def yaml_deserialization(yaml_data):
    return yaml.load(yaml_data)  # Insecure (use safe_load instead)


# ============================================================
# A09:2021 - Security Logging and Monitoring Failures
# ============================================================
def logging_failure():
    try:
        1 / 0
    except Exception as e:
        traceback.print_exc()  # Exposes full stack trace
        logging.info(f"User password failed: {e}")  # Sensitive info logged


# ============================================================
# A10:2021 - Server-Side Request Forgery (SSRF)
# ============================================================
def ssrf_attack():
    url = input("Enter URL: ")  # User-controlled URL
    response = requests.get(url)  # No validation
    return response.text


if __name__ == "__main__":
    app.run()
 
