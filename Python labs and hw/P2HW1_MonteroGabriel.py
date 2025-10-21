# Gabriel Montero
# 10/2/2025
# P2HW1
# This program calculates and displays user imputed values, follows up om P1HW1 and changes how results are displayed


budget= float(input("Enter your Budget: "))
print()
destination= input("Enter your travel Location: ")
print()
Gas= float(input("How much do you think you will spend on gas?: "))
print()
Hotel= float(input("Approximately, how much will you need for for accommodation/hotel?: "))
print()
food= float(input("How much do you need for food: "))
print()
expenses= Gas + Hotel + food
print()
print("----------Travel Expenses---------")
print(f'{"Location: ":<20} {destination}')
print(f'{"Initial Budget:":<20} ${budget:.2f}')
print(f'{"Fuel:":<20} ${Gas:.2f}')
print(f'{"Accommodation:":<20} ${Hotel:.2f}')
print(f'{"Food:":<20} ${food:.2f}')
print("----------------------------------")
print()
print(f'{"Remaining Balance:":<20} ${budget - expenses:.2f}')