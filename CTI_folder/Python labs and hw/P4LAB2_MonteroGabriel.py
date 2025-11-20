#Gabriel Montero
#P4LAB2
#10/28/25

#This programs is to tech me how to use loops (for and while)


#get integer from user
#determine if int is positive or negative
#if positive, display multiplication table
#if negative, tell user program cannot use negative numbers
#if yes, run 
#if no, end program

run_again = 'yes'

while run_again != "no":

    user_num = int(input('Enter and Integer: '))

    if user_num>=0:
        #display multiplication for that value and range (1-12)
        for item in range (1, 13):
            print(f"{user_num} * {item} = {user_num * item}")
        print("\n")
    else:
        print('This program does not handle negative numbers')
        print("\n")
    run_again = input('Would you like to run this program again? ')

#loop has broken, user entered no

print('Program is ending....')









