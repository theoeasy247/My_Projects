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
            print(f"Your balance is {balance}")
        elif choice == "2":
            try:
                amount = int(input("Enter the deposit amount: "))
                if amount > 0:
                    balance = balance + amount
                    print(amount)
                else:
                    print("Zero or negative amounts not allow") 
               
            except ValueError:
                print("You cannot use zero or negetive int.")
    
        elif choice == "3":
            print("Withdraw feature coming next")
        elif choice == "4":
            print("Thank you for using Smart ATM")
            break
