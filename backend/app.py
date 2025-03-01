from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# File to store user credentials
EXCEL_FILE = "users.xlsx"

# Check if the Excel file exists, if not, create it
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Email", "Password"])
    df.to_excel(EXCEL_FILE, index=False)

def read_users():
    """Read users from the Excel file"""
    return pd.read_excel(EXCEL_FILE)

def save_user(email, password):
    """Save user to the Excel file"""
    df = read_users()
    
    # Check if email already exists
    if email in df["Email"].values:
        return False  # User already exists
    
    new_user = pd.DataFrame([[email, password]], columns=["Email", "Password"])
    df = pd.concat([df, new_user], ignore_index=True)
    
    df.to_excel(EXCEL_FILE, index=False)
    return True

def authenticate_user(email, password):
    """Check if user credentials are valid"""
    df = read_users()
    user = df[(df["Email"] == email) & (df["Password"] == password)]
    return not user.empty

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if save_user(email, password):
        return jsonify({"message": "Signup successful!"}), 200
    else:
        return jsonify({"message": "User already exists!"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if authenticate_user(email, password):
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
