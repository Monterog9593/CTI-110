# Gabriel Montero
# 9/18/2025
# P1HW2
# This program calculates and displays user imputed values



budget= int(input("Enter your Budget: "))
print()
destination= input("Enter your travel Location: ")
print()
Gas= int(input("How much do you think you will spend on gas?: "))
print()
Hotel= int(input("Approximately, how much will you need for for accommodation/hotel?: "))
print()
food= int(input("How much do you need for food: "))
print()
expenses= Gas + Hotel + food
print()
print("----------Travel Expenses---------")
print("Location:",destination)
print("Initial Budget:", budget)
print()
print("Fuel:", Gas)
print("Accommodation:",Hotel)
print("Food:", food)
print()
print("Remaining Balance", budget - expenses)






