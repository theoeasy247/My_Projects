from datetime import datetime

now = datetime.now()

date = now.strftime("%d/%m/%Y")
time = now.strftime("%I:%M %p")

print("Date:", date)
print("Time:", time)