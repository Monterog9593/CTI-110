#Gabriel Montero
#P4HW2
#10/28/25

#this program follows up on P3HW3, creating loops to calculate an employees' pay

#Lets gather employee"s name and their pay

total_regular_pay = 0
total_overtime_pay = 0
total_gross_pay = 0
employee_count = 0

# now lets get the loop


while True:
    employee_name = input("Enter employee's name or 'Done' to Terminate: ")  #Input name to start the loop
    if employee_name.lower() == "done":                                      #Input done to stop the loop
        break

    pay_rate = float(input(f"Enter pay rate for {employee_name}: "))         #Get the pay rate and number of hours worked
    hours_worked = float(input(f"Enter hours worked by {employee_name}: "))

    if hours_worked > 40:                                                    #If statement for overtime with an else statement for no overtime
        overtime_hours = hours_worked - 40
        regular_hours = 40
    else:
        overtime_hours = 0
        regular_hours = hours_worked

    regular_pay = regular_hours * pay_rate                                   #Formulas to calculate the pay
    overtime_pay = overtime_hours * (pay_rate * 1.5)
    gross_pay = regular_pay + overtime_pay

    print(f"\nPay Summary for {employee_name}")                              # Print the pay, still need to format (update, Turned the block into comments)
    #print(f"Regular Hours: {regular_hours:.2f}")
    #print(f"Overtime Hours: {overtime_hours:.2f}")
    #print(f"Regular Pay: ${regular_pay:.2f}")
    #print(f"Overtime Pay: ${overtime_pay:.2f}")
    #print(f"Gross Pay: ${gross_pay:.2f}\n")


    print('-----------------------------------------------------------------------------------------') #The format for the output
    print(f'{"Employee name: ":<20} {employee_name}')
    print()
    if overtime_hours == 0:
        print("No overtime pay")
        print()
        print(f"{'Hours Worked':<15} {'Pay Rate':<15} {'RegHour Pay':<15} {'Gross Pay':<15}")
        print('-----------------------------------------------------------------------------------------')
        print(f'{hours_worked:<15} {pay_rate:<15} ${regular_pay:<15.2f} ${gross_pay:<15.2f}')

    else:
        print(f"{'Hours Worked':<15} {'Pay Rate':<15} {'Overtime':<15} {'Overtime Pay':<15} {'RegHour Pay':<15} {'Gross Pay':<15}")
        print('-------------------------------------------------------------------------------------------------------')
        print(f'{hours_worked:<15} {pay_rate:<15} {overtime_hours:<15} {overtime_pay:<15.2f} ${regular_pay:<15.2f} ${gross_pay:<15.2f}')


    total_regular_pay += regular_pay                                       #This part is to allow for the program to loop again as well as getting all employee's pay added
    total_overtime_pay += overtime_pay
    total_gross_pay += gross_pay
    employee_count += 1

print()
print("Summary of All Employees")   #This is for the total pay for all employee's
print()
print(f"Total number of employees entered: {employee_count}")
print(f"Total Regular Pay: ${total_regular_pay:.2f}")
print(f"Total Overtime Pay: ${total_overtime_pay:.2f}")
print(f"Total Gross Pay: ${total_gross_pay:.2f}")
