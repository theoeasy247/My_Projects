from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect("smart_atm.db")
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts (account_id)
        )
    """)

    connection.commit()
    connection.close()

app.secret_key = "smart-atm-development-key"

correct_pin = "2026"
balance = 50000
transaction_history = []

# Homepage and login route
@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    attempts = session.get("attempts", 0)

    if request.method == "POST":

        entered_pin = request.form.get("pin", "").strip()
        
        if attempts >= 3:
            message = "Too many incorrect attempts. Access denied."

        else:
            if entered_pin == correct_pin:
                session["attempts"] = 0
                session["logged_in"] = True
                return redirect(url_for("dashboard"))

            else:
                attempts += 1
                session["attempts"] = attempts

                message = "Incorrect PIN. Please try again."

                if attempts >= 3:
                    message = "Too many incorrect attempts. Access denied."

    return render_template("index.html", message=message)

@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html", 
        balance=balance,
        transaction_history=transaction_history
    )

@app.route("/deposit", methods=["POST"])
def deposit():
    global balance

    if not session.get("logged_in"):
        return redirect(url_for("home"))

    amount = request.form.get("amount", "").strip()

    try:
        amount = int(amount)

        if amount > 0:
            balance += amount
            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y %I:%M %p")

            transaction_history.append({
                "type": "Deposit",
                "amount": amount,
                "timestamp": timestamp
            })
            
            message = "Deposit successful!"
            message_type = "success"

        else:
            message = "Deposit amount must be greater than zero."
            message_type = "error"
    except ValueError:
        message = "Please enter a valid whole number."
        message_type = "error"

    return render_template(
        "dashboard.html",
        balance=balance,
        message=message,
        message_type=message_type,
        transaction_history=transaction_history
    )

@app.route("/withdraw", methods=["POST"])
def withdraw():
    global balance

    if not session.get("logged_in"):
        return redirect(url_for("home"))

    amount = request.form.get("amount", "").strip()

    try:
        amount = int(amount)

        if amount <= 0:
            message = "Withdrawal amount must be greater than zero."
            message_type = "error"
        elif amount > balance:
            message = "Insufficient funds. Your balance is too low."
            message_type = "error"
        else:
            balance -= amount
            now = datetime.now()
            timestamp = now.strftime("%d/%m/%Y %I:%M %p")

            transaction_history.append({
                "type": "Withdrawal",
                "amount": amount,
                "timestamp": timestamp
            })
            message = "Withdrawal successful!"
            message_type = "success"

    except ValueError:
        message = "Please enter a valid whole number."
        message_type = "error"

    return render_template(
        "dashboard.html",
        balance=balance,
        message=message,
        message_type=message_type,
        transaction_history=transaction_history
    )

# Run the Flask application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
