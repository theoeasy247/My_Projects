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

#cursor.execute("""
   # INSERT INTO accounts (account_name, balance)
   # VALUES (?, ?)
#""", ("Theoeasy", 50000))

# connection.commit()

cursor.execute(
    "UPDATE accounts SET balance = ? WHERE account_id = ?",
    (55000, 1)
)

cursor.execute(
    "DELETE FROM accounts WHERE account_id = ?",
    (9,)
)

connection.commit()

print("Account deleted successfully!")

cursor.execute("SELECT COUNT(*) FROM accounts")

total_accounts = cursor.fetchone()

print("TOTAL ACCOUNTS:")
print(total_accounts)

cursor.execute("SELECT SUM(balance) FROM accounts")

total_balance = cursor.fetchone()

print("TOTAL MONEY IN ATM:")
print(total_balance)


cursor.execute("SELECT AVG(balance) FROM accounts")

average_balance = cursor.fetchone()

print("AVERAGE ACCOUNT BALANCE:")
print(average_balance)

connection.commit()

print("Account balance updated successfully!")

cursor.execute("SELECT * FROM accounts")

accounts = cursor.fetchall()

print("ATM ACCOUNT RECORDS:")

for account in accounts:
    print(account)


cursor.execute(
    "SELECT * FROM accounts WHERE account_id = ?",
    (1,)
)

account = cursor.fetchone()

print("SPECIFIC ACCOUNT:")
print(account)