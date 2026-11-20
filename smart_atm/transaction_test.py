import sqlite3

connection = sqlite3.connect("transaction_practice.db")

cursor = connection.cursor()


try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_accounts(
        account_id INTEGER PRIMARY KEY,
        account_name TEXT NOT NULL, 
        balance INTEGER NOT NULL
    )
""")
    cursor.execute("""
        INSERT OR IGNORE INTO practice_accounts
        (account_id, account_name, balance)
        VALUES (?, ?, ?)
    """, (1, "Theoeasy", 5000))

    cursor.execute(
        "UPDATE practice_accounts SET balance = balance + ? WHERE account_id = ?",
        (100, 1)
    )

    print("account balance updated successufully!")
    
    cursor.execute("UPDATE wrong_table SET balance = 0")
    
    connection.commit()

except sqlite3.Error as error:
    connection.rollback()
    print("Database error:", error)

finally:
    connection.close()
    print("Database connection closed.")