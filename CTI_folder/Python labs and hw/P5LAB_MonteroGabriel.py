#Gabriel Montero
#11/11/25
#P5LAB
#Customer self checkout simulation

import random

#follow up to P3LAB1
def disperse_change(change):
    change = round(change*100)
    #Dollar
    dollar = change//100
    change = change - (dollar*100)
    #quarters
    quarters = change//25
    change = change - (quarters*25)
    #dimes
    dimes = change//10
    change = change - (dimes*10)
    #nickles
    nickles = change//5
    change = change - (nickles*5)
    #pennies
    pennies = change
    if dollar > 0:
        if dollar == 1:
            print(f'{dollar} Dollar')
        else:
            print(f'{dollar} Dollars')
    if quarters > 0:
        if quarters == 1:
            print(f'{quarters} Quarter')
        else:
            print(f'{quarters} Quarters')
    if dimes > 0:
        if dimes == 1:
            print(f'{dimes} Dime')
        else:
            print(f'{dimes} Dimes')
    if nickles > 0:
        if nickles == 1:
            print(f'{nickles} Nickle')
        else:
            print(f'{nickles} Nickels')
    if pennies > 0:
        if pennies == 1:
            print(f'{pennies} Penny')
        else:
            print(f'{pennies} Pennies')


def main ():
    #logic goes here
    
    #generate the amount owed
    amount_owed = round(random.uniform(0.01, 100.00), 2)
    print(f'You owe: ${amount_owed}')
    
    
    #create variable for money into machine
    money_in = float(input('How Much cash will you put into the self-checkout? '))
    
    #Calculate change owed to customer
    change = money_in - amount_owed
    print(f'Change is: ${change:.2f}')
    print()
    #call disperse change function
    disperse_change(change)





#call the main function
main()