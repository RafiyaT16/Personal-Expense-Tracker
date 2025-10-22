from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",   
        database="expense_db"
    )

DATA_FILE = "data.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        expenses = json.load(f)
else:
    expenses = []
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

@app.route("/add", methods=["POST"])
def add_expense():
    try:
        data = request.get_json(force=True)
        category = data.get("category")
        amount = data.get("amount")
        date = data.get("date")
        if not category or not amount or not date:
            return jsonify({"error": "Missing fields"}), 400
        expense = {"category": category, "amount": amount, "date": date}
        expenses.append(expense)
        with open(DATA_FILE, "w") as f:
            json.dump(expenses, f, indent=2)
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)"
        cursor.execute(sql, (category, amount, date))
        conn.commit()
        cursor.close()
        conn.close()
        print("Saved to JSON and MySQL")
        return jsonify({"message": "Expense added successfully"}), 200
    except Exception as e:
        print("Error adding expense:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses), 200

@app.route("/clear", methods=["DELETE"])
def clear_expenses():
    global expenses
    expenses = []
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    return jsonify({"message": "All expenses cleared"}), 200

if __name__ == "__main__":
    app.run(debug=True)
