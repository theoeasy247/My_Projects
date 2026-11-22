
import sqlite3

connection = sqlite3.connect("smart_atm.db")
connection.execute("PRAGMA foreign_keys = ON")


# TEST 1: Negative account balance
connection.execute("SAVEPOINT test1")

try:
    connection.execute(
        "UPDATE accounts SET balance = -500 WHERE account_id = 1"
    )
    print("FAIL: Negative balance was accepted.")

except sqlite3.IntegrityError:
    print("PASS: Negative balance rejected.")

finally:
    connection.execute("ROLLBACK TO test1")
    connection.execute("RELEASE test1")


# TEST 2: Zero transaction amount
connection.execute("SAVEPOINT test2")

try:
    connection.execute("""
        INSERT INTO transactions
        (account_id, transaction_type, amount, timestamp)
        VALUES (1, 'Deposit', 0, 'Test')
    """)
    print("FAIL: Zero transaction amount was accepted.")

except sqlite3.IntegrityError:
    print("PASS: Zero transaction amount rejected.")

finally:
    connection.execute("ROLLBACK TO test2")
    connection.execute("RELEASE test2")


# TEST 3: Invalid transaction type
connection.execute("SAVEPOINT test3")

try:
    connection.execute("""
        INSERT INTO transactions
        (account_id, transaction_type, amount, timestamp)
        VALUES (1, 'Transfer', 100, 'Test')
    """)
    print("FAIL: Invalid transaction type was accepted.")

except sqlite3.IntegrityError:
    print("PASS: Invalid transaction type rejected.")

finally:
    connection.execute("ROLLBACK TO test3")
    connection.execute("RELEASE test3")


# TEST 4: Non-existing customer account
connection.execute("SAVEPOINT test4")

try:
    connection.execute("""
        INSERT INTO transactions
        (account_id, transaction_type, amount, timestamp)
        VALUES (999999, 'Deposit', 100, 'Test')
    """)
    print("FAIL: Invalid customer account was accepted.")

except sqlite3.IntegrityError:
    print("PASS: Invalid customer account rejected.")

finally:
    connection.execute("ROLLBACK TO test4")
    connection.execute("RELEASE test4")


connection.close()
