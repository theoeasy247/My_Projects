import sqlite3

connection = sqlite3.connect("practice.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY,
        account_name TEXT NOT NULL,
        balance INTEGER NOT NULL
    )
""")

connection.commit() 

cursor.execute("""
    INSERT OR IGNORE INTO accounts
    (account_id, account_name, balance)
    VALUES (?, ?, ?)
""", (1, "Theoeasy", 50000))

connection.commit()

cursor.execute(
    "SELECT * FROM accounts WHERE account_id = ?",
    (1,)
)

account = cursor.fetchone()

print(account)

connection.execute("BEGIN")

cursor.execute(
    "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
    (5000, 1)
)

cursor.execute(
    "SELECT balance FROM accounts WHERE account_id = ?",
    (1,)
)

print("Balance inside transaction:", cursor.fetchone()[0])

connection.rollback()

print("Transaction rolled back!")

print("Transaction committed successfully!")

connection.close()