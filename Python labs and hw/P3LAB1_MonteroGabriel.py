#Gabriel Montero
#P3LAB1
#10/9/25
#program allows user to enter money value, then efficiently return with coin values

# first draft attempt
#money = float(input('Enter the amount of money as a float: $'))

#left = int(money*100)
#print(left)
#dollars = left//100
#print("removed", dollars, "dollars")
#left = left%100
#print(left)
#quarters = left//25
#dimes = left//10
#nickels = left//5
#pennies = left//1
#if money == 0:
    #print('no Change')
#if dollars >= 0:
    #print(dollars, 'Dollars')
#if quarters >= 0:
    #print(quarters, 'Quarters')
#if dimes >= 0:
    #print(dimes, 'Dimes')
#if nickels >= 0:
    #print(nickels, 'Nickles')
#if pennies >= 0:
    #print(pennies, 'Pennies')


# second attempt with the lecture video

change = float(input('Enter amount of money as a float: $ '))

#print(f'Change amount {money_input}')

#float to integer
change = int(change*100)

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