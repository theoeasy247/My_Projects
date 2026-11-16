import sqlite3

# Connect to the ATM database
connection = sqlite3.connect("atm.db")

# Create a database cursor
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_name TEXT NOT NULL,
        balance INTEGER NOT NULL
    )
""")

connection.commit()

cursor.execute("""
    INSERT INTO accounts (account_name, balance)
    VALUES (?, ?)
""", ("Theoeasy", 50000))

connection.commit()

cursor.execute("SELECT * FROM accounts")
cursor.execute(
    "SELECT * FROM accounts WHERE account_id = ?",
    (1,)
)

account = cursor.fetchone()

print("SPECIFIC ACCOUNT:")
print(account)

accounts = cursor.fetchall()

print("ATM ACCOUNT RECORDS:")

for account in accounts:
    print(account)

print("Account registered successfully!")

print("Accounts table created successfully!")

print("Database connected successfully!")

# Close the connection
connection.close()

print("Database connection closed.")