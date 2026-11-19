from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime
import sqlite3
import hashlib
import secrets
import hmac


app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("smart_atm.db")
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def hash_pin(pin):
    salt = secrets.token_bytes(16)

    pin_hash = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex() + ":" + pin_hash.hex()

def verify_pin(pin, stored_hash):
    salt_hex, hash_hex = stored_hash.split(":")
    salt = bytes.fromhex(salt_hex)

    new_hash = hashlib.pbkdf2_hmac(
    "sha256",
    pin.encode("utf-8"),
    salt,
    600000
)
    return hmac.compare_digest(new_hash.hex(), hash_hex)

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

# Customer registration route
@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        account_name = request.form.get("account_name", "").strip()
        pin = request.form.get("pin", "").strip()
        confirm_pin = request.form.get("confirm_pin", "").strip()

        if not account_name:
            message = "Please enter your full name."

        elif len(pin) != 4 or not pin.isdigit():
            message = "PIN must contain exactly 4 digits."

        elif pin != confirm_pin:
            message = "Your PINs do not match."

        else:
            pin_hash = hash_pin(pin)

            connection = get_db_connection()

            cursor = connection.execute(
                """
                INSERT INTO accounts (account_name, pin_hash, balance)
                VALUES (?, ?, ?)
                """,
                (account_name, pin_hash, 0)
            )

            connection.commit()

            account_id = cursor.lastrowid

            connection.close()

            message = f"Account created successfully! Your Account ID is {account_id}."

    return render_template("register.html", message=message)

# Homepage and login route
@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    attempts = session.get("attempts", 0)

    if request.method == "POST":

        account_id = request.form.get("account_id", "").strip()
        entered_pin = request.form.get("pin", "").strip()
        
        if attempts >= 3:
            message = "Too many incorrect attempts. Access denied."

        else:

            try:
                account_id = int(account_id)

                connection = get_db_connection()

                account = connection.execute(
                    "SELECT * FROM accounts WHERE account_id = ?",
                    (account_id,)
                ).fetchone()

                connection.close()

            except ValueError:
                account = None

            if account and verify_pin(entered_pin, account["pin_hash"]):

                session["attempts"] = 0
                session["logged_in"] = True
                session["account_id"] = account["account_id"]
                session["account_name"] = account["account_name"]

                return redirect(url_for("dashboard"))

            else:
                attempts += 1
                session["attempts"] = attempts

                message = "Incorrect Account ID or PIN. Please try again."

                if attempts >= 3:
                    message = "Too many incorrect attempts. Access denied."

    return render_template("index.html", message=message)


# Customer-specific dashboard route
@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("home"))

    account_id = session.get("account_id")

    connection = get_db_connection()

    account = connection.execute(
        "SELECT * FROM accounts WHERE account_id = ?",
        (account_id,)
    ).fetchone()

    print("DEBUG Account ID:", account_id)
    print("DEBUG Database Account:", dict(account) if account else None)

    if account is None:
        connection.close()
        session.clear()
        return redirect(url_for("home"))

    transactions = connection.execute(
        """
        SELECT transaction_type, amount, timestamp
        FROM transactions
        WHERE account_id = ?
        ORDER BY transaction_id DESC
        """,
        (account_id,)
    ).fetchall()

    connection.close()

    transaction_history = [
        {
            "type": transaction["transaction_type"],
            "amount": transaction["amount"],
            "timestamp": transaction["timestamp"]
        }
        for transaction in transactions
    ]

    return render_template(
        "dashboard.html",
        account_name=account["account_name"],
        balance=account["balance"],
        transaction_history=transaction_history
    )


# Customer logout route
@app.route("/logout")
def logout():

    session.clear()

    flash("You have successfully logged out.", "success")

    return redirect(url_for("home"))


@app.route("/deposit", methods=["POST"])
def deposit():

    if not session.get("logged_in"):
        return redirect(url_for("home"))

    account_id = session.get("account_id")
    amount = request.form.get("amount", "").strip()

    try:
        amount = int(amount)

        if amount <= 0:
            flash("Deposit amount must be greater than zero.", "error")
            return redirect(url_for("dashboard"))

        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y %I:%M %p")

        connection = get_db_connection()

        connection.execute(
            """
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_id = ?
            """,
            (amount, account_id)
        )

        connection.execute(
            """
            INSERT INTO transactions
            (account_id, transaction_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (account_id, "Deposit", amount, timestamp)
        )

        connection.commit()
        connection.close()

        flash("Deposit successful!", "success")

    except ValueError:
        flash("Please enter a valid whole number.", "error")

    return redirect(url_for("dashboard"))


@app.route("/withdraw", methods=["POST"])
def withdraw():
    global balance

    if not session.get("logged_in"):
        return redirect(url_for("home"))

    account_id = session.get("account_id")
    amount = request.form.get("amount", "").strip()

    try:
        amount = int(amount)

        if amount <= 0:
            flash("Withdrawal amount must be greater than zero.")
            return redirect(url_for("dashboard"))
        
        connection = get_db_connection()

        account = connection.execute(
            "SELECT balance FROM accounts WHERE account_id = ?",
            (account_id,)
        ).fetchone()

        if account is None:
            connection.close()
            session.clear()
            return redirect(url_for("home"))

        if amount > account["balance"]:
            connection.close()
            flash("Insufficient funds. Your balance is too low.", "error")
            return redirect(url_for("dashboard"))
        
        now = datetime.now()
        timestamp = now.strftime("%d/%m/%Y %I:%M %p")

        connection.execute(
            """
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_id = ?
            """,
            (amount, account_id)
        )

        connection.execute(
            """
            INSERT INTO transactions
            (account_id, transaction_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (account_id, "Withdrawal", amount, timestamp)
        )

        connection.commit()
        connection.close()
        
        flash("Withdrawal successful!", "success")

    except ValueError:
        flash("Please enter a valid whole number.", "error")

    return redirect(url_for("dashboard"))


# Run the Flask application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
