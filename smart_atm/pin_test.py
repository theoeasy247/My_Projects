from app import hash_pin, verify_pin

stored_hash = hash_pin("2026")

print("Correct PIN:", verify_pin("2026", stored_hash))
print("Wrong PIN:", verify_pin("1234", stored_hash))