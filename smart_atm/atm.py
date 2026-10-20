correct_pin = "2026"
attempts_counter = 0
max_attempts = 3
entered_pin = (input("Enter your pin: "))

attempts = 0
while attempts < 3:
    print("You can enter your PIN")
    attempts = attempts + 1

if entered_pin == correct_pin:
    print("PIN accepted")
else:
    print("Incorrect PIN")