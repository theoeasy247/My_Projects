correct_pin = "2026"
balance = 50000
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
"""

if authenticated:
    while True:
        print(MENU)
        choice = input("Select an option (1-4):").strip()

        if choice == "1":
            print(f"Your balance is ₦{balance}")
        elif choice == "2":
            try:
                amount = int(input("Enter the deposit amount: "))
                if amount > 0:
                    balance = balance + amount
                    print(f"Deposit successful: {amount}")
                    print(f"Your new balance is: ₦{balance}")
                else:
                    print("Invalid deposit. Amount must be greater than zero.") 
               
            except ValueError:
                print("input must be a valid whole number")
    
        elif choice == "3":
            try:
                withdrawal_amount = int(input("Enter withdrawal amount: "))
                if withdrawal_amount > 0. or negative:
                    print("Invalid Amount. Amount must be greater than zero.") 

                if withdrawal_amount <= balance:
                    balance = balance - withdrawal_amount
                    print(f"Withdrawal is successful: {withdrawal_amount}")
                    print(f"Your new balance is: {balance}")
            
            except ValueError:
                print("input must be a valid whole number")

        elif choice == "4":
            print("Thank you for using Smart ATM")
            break
