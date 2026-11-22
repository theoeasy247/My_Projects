
import sqlite3

connection = sqlite3.connect("smart_atm.db")

try:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("BEGIN")

    # Create the improved accounts table
    connection.execute("""
        CREATE TABLE accounts_new (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            pin_hash TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0
                CHECK (balance >= 0)
        )
    """)

    # Create the improved transactions table
    connection.execute("""
        CREATE TABLE transactions_new (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL
                CHECK (transaction_type IN ('Deposit', 'Withdrawal')),
            amount INTEGER NOT NULL
                CHECK (amount > 0),
            timestamp TEXT NOT NULL,
            FOREIGN KEY (account_id)
                REFERENCES accounts_new (account_id)
        )
    """)

    # Copy existing customer records
    connection.execute("""
        INSERT INTO accounts_new
        SELECT * FROM accounts
    """)

    # Copy existing transaction records
    connection.execute("""
        INSERT INTO transactions_new
        SELECT * FROM transactions
    """)

    # Remove old tables, child table first
    connection.execute("DROP TABLE transactions")
    connection.execute("DROP TABLE accounts")

    # Give the new tables their original names
    connection.execute(
        "ALTER TABLE accounts_new RENAME TO accounts"
    )

    connection.execute(
        "ALTER TABLE transactions_new RENAME TO transactions"
    )

    # Verify foreign key relationships
    violations = connection.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    if violations:
        raise sqlite3.IntegrityError(
            f"Foreign key violations: {violations}"
        )

    connection.commit()

    print("Database migration completed successfully!")

except Exception as error:
    connection.rollback()
    print("Migration failed:", error)

finally:
    connection.close()
