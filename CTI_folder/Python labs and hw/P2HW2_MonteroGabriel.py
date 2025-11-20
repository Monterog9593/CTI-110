
# Gabriel Montero
# P2HW2
# 10/4/2025
# Program performs calculations using (in this case) grades inputted from the user

# Get the grades from the user
mod1 = float(input("Enter grade for Module 1: "))
mod2 = float(input("Enter grade for Module 2: "))
mod3 = float(input("Enter grade for Module 3: "))
mod4 = float(input("Enter grade for Module 4: "))
mod5 = float(input("Enter grade for Module 5: "))
mod6 = float(input("Enter grade for Module 6: "))

grades = [mod1, mod2, mod3, mod4, mod5, mod6]

# print(grades)- tested to see if the grades input affected the list

# Create a sum value and a average value

sum = (mod1+mod2+mod3+mod4+mod5+mod6)
avg = sum/6 #I picked six since 2 were in this example
#Code below when ran gets the sum and avg of the list of grades
#print(f"{sum:.2f}")
#print(f"{avg:.2f}")

#Now to extract the lowest and highest grades from the list, looked up min/max codes

lowest_grade= min(grades)
highest_grade= max(grades)
#Print statement below shows how to get the highest grades and lowest grades from list
#print(lowest_grade)
#print(highest_grade)

#Now to code the the output, remember how to format it like in P2HW1

print("-------------Results----------")
print(f'{"Lowest Grade: ":<20} {lowest_grade:.1f}')
print(f'{"Highest Grade: ":<20} {highest_grade:.1f}')
print(f'{"Sum of Grades: ":<20} {sum:.1f}')
print(f'{"Average Grade: ":<20} {avg:.2f}')
print("------------------------------")