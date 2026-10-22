correct_pin = "2026"
balance = 50000
transaction_history = []
attempts = 0
max_attempts = 3
authenticated = False

while attempts < max_attempts and not authenticated:
    entered_pin = input("Enter your PIN: ")

    if entered_pin == correct_pin:
        authenticated = True
        print("PIN accepted")
    else:
        attempts = attempts + 1
        print("Incorrect PIN")
        
if not authenticated:
     print("Access denied") 

MENU = """
===== SMART ATM =====
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Exit
5. View Transaction History
"""

if authenticated:
    while True:
        print(MENU)
        choice = input("Select an option (1-5):").strip()

        if choice == "1":
            print(f"Your balance is ₦{balance}")
        elif choice == "2":
            try:
                amount = int(input("Enter the deposit amount: "))
                if amount > 0:
                    balance = balance + amount
                    transaction_history.append(f"Deposit: ₦{amount}")
                    print(f"Deposit successful: ₦{amount}")
                    print(f"Your new balance is: ₦{balance}")
                    
                else:
                    print("Invalid deposit. Amount must be greater than zero.") 
               
            except ValueError:
                print("input must be a valid whole number")
    
        elif choice == "3":
            try:
                withdrawal_amount = int(input("Enter withdrawal amount: "))
                if withdrawal_amount <= 0:
                    print("Invalid Amount. Amount must be greater than zero.") 

                elif withdrawal_amount > balance:
                    print("Insuficient funds")
                
                else:
                    balance = balance - withdrawal_amount
                    print(f"Withdrawal is successful: ₦{withdrawal_amount}")
                    print(f"Your new balance is: ₦{balance}")
                    transaction_history.append(f"Withdrawal: ₦{withdrawal_amount}")
            
            except ValueError:
                print("input must be a valid whole number")

        elif choice == "4":
            print("Thank you for using Smart ATM")
            break

        elif choice == "5":
            print("===== TRANSACTION HISTORY =====")
            total_deposits = 0
            total_withdrawals = 0

            for transaction in transaction_history:
                if transaction.startswith("Deposit"):
                    deposit_amount + total_deposits
                    pass
                elif transaction.startswith("Withdrawal"):
                    withdrawal_amount + total_withdrawals
                    pass
                    
            if not transaction_history:
                print("No transactions yet")

            else:
                for transaction in transaction_history:
                    print(transaction)

        else:
                print("Invalid choice. please select 1-5")

     
           