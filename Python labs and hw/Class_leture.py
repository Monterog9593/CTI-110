#Class code with professor
#10/7/25
#Mr. Teter teaches us about if and else statements.
#Program calculates Area of rectangle
#*******************Pseudocode********************
# Display 'This program calculates area of rectangle'
#input length
#length= float(input("Please Enter Rectangle Length: "))
#input width
#width= float(input("Please Enter Rectangle Width: "))
#area equation
#area= length*width
import math


print("This program Calculates the Area of a Rectangle")
print("Please input values below.")
print("-----------------------------------------")
#The values needed for the program
length = float(input("Please Enter Rectangle Length: "))
width = float(input("Please Enter Rectangle Width: "))
area = length * width
#Output displayed to user, this is the standard output 
#print(f"Length entered: {length}")
#print(f"Width entered: {width}")
#print("-----------------------------------------")
#Display the area with: print(f"The Area of the rectangle is: {area:.2f}")
#print(f"The Area of the rectangle is: {area:.2f}")


#Now we make decision structures for the program
#if statement haves conditions
if width > length:
    print("-----------------------------------------")
    print('\n~~ Length should be >= Width')
    print('\n~~ Run program Again for Correct Output')

elif width == length:
    print("-----------------------------------------")
    print(f'\n~~ Length and Width are the same: {length}' )
    print(f'\n~~ This a Square, with an Area of: {area:.2f}' )

else:
    print(f"Length entered: {length}")
    print(f"Width entered: {width}")
    print("-----------------------------------------")
    print(f"The Area of the rectangle is: {area:.2f}")


