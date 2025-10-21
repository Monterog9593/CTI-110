#Gabriel Montero
#10/16/25
#P3HW2
#This program is to calculate overtime pay rate using branching if\else statements

#Get basic information
name = input("Enter employee's name: ")
hours = float(input('Enter number of hours worked: '))
pay_rate = float(input("Enter employee's pay rate: "))


#overtime is hours pass 40
overtime = hours%40
#overtime pay is rate of pay*hour over 40*1.5
ot_pay = (overtime*pay_rate)*1.5
#regular pay is 40*pay rate
reg_pay = pay_rate*40
#gross pay is the total payment
gross = reg_pay+ot_pay










print('------------------------------------------')
print(f'{"Employee name: ":<20} {name}')
print()
#print(f'{"Hours worked: ":<20} {hours:.1f}')
#print(f'{"Pay Rate: ":<20} {pay_rate:.1f}')
#print(f'{"Overtime: ":<20} {overtime:.1f}')
#print(f'{"Overtime pay: ":<20} {ot_pay:.2f}')
#print(f'{"Regular Hour pay: ":<20} {reg_pay:.2f}')
#print(f'{"Gross pay: ":<20} {gross:.2f}')

if overtime == 0:
    print("No overtime")
    print(f"{'Hours Worked':<15} {'Pay Rate':<15} {'RegHour Pay':<15} {'Gross Pay':<15}")
    print('-----------------------------------------------------------------------------------------')
    print(f'{hours:<15} {pay_rate:<15} ${reg_pay:<15.2f} ${gross:<15.2f}')

else:
    print(f"{'Hours Worked':<15} {'Pay Rate':<15} {'Overtime':<15} {'Overtime Pay':<15} {'RegHour Pay':<15} {'Gross Pay':<15}")
    print('-------------------------------------------------------------------------------------------------------')
    print(f'{hours:<15} {pay_rate:<15} {overtime:<15} {ot_pay:<15.2f} ${reg_pay:<15.2f} ${gross:<15.2f}')

#print(f"{'Hours Worked':<15} {'Pay Rate':<15} {'Overtime':<15} {'Overtime Pay':<15} {'RegHour Pay':<15} {'Gross Pay':<15}")
#print('-------------------------------------------------------------------------------------------------------')
#print(f'{hours:<15} {pay_rate:<15} {overtime:<15} {ot_pay:<15.2f} ${reg_pay:<15.2f} ${gross:<15.2f}')