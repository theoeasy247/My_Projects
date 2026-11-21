import sqlite3

connection = sqlite3.connect("rollback_test.db")
connection.row_factory = sqlite3.Row

try:
    connection.execute("BEGIN")

    account = connection.execute(
        "SELECT balance FROM accounts WHERE account_id = 1"
    ).fetchone()

    if account is None:
        print("Account not found.")
    else:
        print("Balance before:", account["balance"])
        connection.execute(
            "UPDATE accounts SET balance = balance - ? WHERE account_id = ?",
            (500, 1)
        )

        print("Balance after deduction:", connection.execute(
            "SELECT balance FROM accounts WHERE account_id = 1"
        ).fetchone()["balance"])

        # Deliberately trigger a database error
        connection.execute("UPDATE wrong_table SET balance = 0")

except sqlite3.Error as error:
    connection.rollback()
    print("Database error:", error)
    print("Rollback executed!")

finally:
    connection.close()