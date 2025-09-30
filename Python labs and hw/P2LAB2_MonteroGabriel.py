# Gabriel Montero
# 9/26/2025
# P2LAB2
# This program Creates a dictionary and use the dictionary values 
# Followed the tutorial video in the module, Thanks

cars= {"Camero": 18.21, "Prius": 52.36, "Model S": 110, "Silverado": 26}
#get keys from the dict
print()
cars_keys= cars.keys()

print(cars_keys)
print(*cars_keys, sep = ",")
#get a car from user
print()
car_name = input("Enter a vehicle to see it's mpg: ")
#get mpg for the given car
print()
car_mpg = cars[car_name]
print(f"The {car_name} gets {car_mpg} miles per gallon.")
print()
#Get miles from User
miles_driven= float(input(f"How many miles will you drive the {car_name}?: "))
print()
#calculate miles and gas
gallons_needed = miles_driven/car_mpg
print()
#display results
print(f"{gallons_needed:.2f} gallon(s) of gas are needed to drive the {car_name} {miles_driven} miles.")