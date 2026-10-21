correct_pin = "2026"
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
