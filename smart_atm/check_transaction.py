import sqlite3

connection = sqlite3.connect("transaction_practice.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM practice_accounts")

account = cursor.fetchone()

print(account)

connection.close()