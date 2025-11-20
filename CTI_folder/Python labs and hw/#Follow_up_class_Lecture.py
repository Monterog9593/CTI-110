#Follow up class Lecture
#10/7/25
#Another math equation but with 3 value instead
#This time a rectangular prism
base = float(input("Enter the Base of the rectangular prism: "))
width = float(input("Enter the Width of the rectangular prism: "))
height = float(input("Enter the Height of the rectangular prism: "))
area = base * width * height
print('---------------------------------')
#print(f'Base entered: {base}')
#print(f'Width entered: {width}')
#print(f'Height entered: {height}')
#print('---------------------------------')
#print(f'The Area Of the Rectangular Prism is: {area:.2f}')

if width > height:
    print('\n~~ Height should be >= Width')
    print('\n~~ Run program Again for Correct Output')
    print("-----------------------------------------")

elif width == height == base:
    print(f'\n~~ Length, Width, and Base are the same: {height}' )
    print(f'\n~~ This a Cube, with an Area of: {area:.2f}' )
    print("-----------------------------------------")

else:
    print(f'Base entered: {base}')
    print(f"Height entered: {height}")
    print(f"Width entered: {width}")
    print("-----------------------------------------")
    print(f"The Area of the rectangular prism is: {area:.2f}")