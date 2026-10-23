Test Directories 

# Smart ATM Simulation

# Project Description
The Smart ATM is a beginner-friendly Python program that simulates basic ATM operations. It allows users to authenticate with a PIN, check their balance, deposit money, withdraw money, and view transaction history.

# Features
- PIN authentication with a maximum of three attempts.
- Check account balance.
- Deposit money with input validation.
- Withdraw money with input validation and insufficient-funds checks.
- Reject invalid menu choices.
- Record successful deposits and withdrawals.
- Display transaction history.
- Calculate total deposits and withdrawals.
- Display the current balance.
- Handle invalid numeric input without crashing.

# Starting Balance
The account starts with a balance of ₦50,000.

# Requirements
- Python 3
- A terminal or command prompt

# How to Run
1. Open a terminal.
2. Navigate to the project directory:

   ```bash
   cd ~/My_Projects/smart_atm
   ```

3. Run the program:

   ```bash
   python3 atm.py
   ```

4. Enter the correct PIN when prompted and follow the menu instructions.

# Testing
The program has been tested for:
- Correct and incorrect PINs.
- Maximum PIN attempts.
- Balance checking.
- Successful deposits and withdrawals.
- Zero and negative transaction amounts.
- Withdrawals exceeding the available balance.
- Invalid menu choices.
- Transaction history and totals.
- Correct balance updates after transactions.

# Important Note
This is an educational simulation. It does not connect to a real bank account, and transaction history is stored only while the program is running.