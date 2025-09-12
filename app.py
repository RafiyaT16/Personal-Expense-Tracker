from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",  
        database="sqlpro"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/categories", methods=["GET"])
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return jsonify(categories)

@app.route("/transactions", methods=["GET"])
def get_transactions():
    user_id = request.args.get("user_id", type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if user_id:
        cursor.execute("""
            SELECT t.transaction_id, u.name, c.category_name, t.amount, t.date, 
                   t.payment_method, t.note
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN categories c ON t.category_id = c.category_id
            WHERE t.user_id = %s
            ORDER BY t.date DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT t.transaction_id, u.name, c.category_name, t.amount, t.date, 
                   t.payment_method, t.note
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN categories c ON t.category_id = c.category_id
            ORDER BY t.date DESC
        """)
    transactions = cursor.fetchall()
    conn.close()
    return jsonify(transactions)

@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    user_id = data["user_id"]
    category_id = data["category_id"]
    amount = data["amount"]
    date = data["date"]
    payment_method = data.get("payment_method", "cash")
    note = data.get("note", "")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, category_id, amount, date, payment_method, note)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, category_id, amount, date, payment_method, note))
    conn.commit()
    conn.close()
    return jsonify({"message": "Transaction added successfully!"})

@app.route("/budgets", methods=["GET"])
def get_budgets():
    user_id = request.args.get("user_id", type=int)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if user_id:
        cursor.execute("""
            SELECT b.budget_id, u.name, c.category_name, b.amount_limit, b.month, b.year
            FROM budgets b
            JOIN users u ON b.user_id = u.user_id
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.user_id = %s
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT b.budget_id, u.name, c.category_name, b.amount_limit, b.month, b.year
            FROM budgets b
            JOIN users u ON b.user_id = u.user_id
            JOIN categories c ON b.category_id = c.category_id
        """)
    budgets = cursor.fetchall()
    conn.close()
    return jsonify(budgets)

@app.route("/add", methods=["POST"])
def add_expense_simple():
    data = request.get_json()
    category = data["category"]
    amount = data["amount"]
    date = data["date"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, category_id, amount, date, payment_method, note)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (1, 1, amount, date, "cash", category))
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense added successfully!"})

@app.route("/expenses", methods=["GET"])
def get_expenses_simple():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.category_name AS category, t.amount, t.date
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
        ORDER BY t.date DESC
    """, (1,))
    expenses = cursor.fetchall()
    conn.close()
    return jsonify(expenses)


@app.route("/budgets", methods=["POST"])
def add_budget():
    data = request.get_json()
    user_id = data["user_id"]
    category_id = data["category_id"]
    amount_limit = data["amount_limit"]
    month = data["month"]
    year = data["year"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO budgets (user_id, category_id, amount_limit, month, year)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, category_id, amount_limit, month, year))
    conn.commit()
    conn.close()
    return jsonify({"message": "Budget added successfully!"})

@app.route("/analytics/expense_summary", methods=["GET"])
def expense_summary():
    user_id = request.args.get("user_id", type=int)
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.category_name, SUM(t.amount) AS total_spent
        FROM transactions t
        JOIN categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s AND c.type = 'expense' 
              AND MONTH(t.date) = %s AND YEAR(t.date) = %s
        GROUP BY c.category_name
    """, (user_id, month, year))
    summary = cursor.fetchall()
    conn.close()
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=True)
