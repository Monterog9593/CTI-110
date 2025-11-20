#Gabriel Montero
#P4HW1
#10/2802025
#Building off of P2HW2, progaram will ue loops to calculate average

#(import P2HW2_MonteroGabriel) #import the code since it is already done


#for this purpose write out a new code for branching and pathing for the code

#Collect grades from the user by creating a list

num_grades = int(input('How many scores do you want to enter?: ')) #how many grades they are going to use 
scores = [] #the list, filled by the number that they asked for
count = 0 #This is the value used for incrementing the scores gathered

#Below is the loop used for gathering the grades

while count < num_grades:
    score = float(input(f"Enter score #{count + 1}: "))
    if score >= 0:
            scores.append(score)
            count += 1
    else:
        print("Invalid score!!! Score should be between 0 and 100.")

sum = sum(scores) #sum of their grades
avg = sum/len(scores) #average grade divided by the the number of scores collected.

grade_drop = min(scores) #the lowest grade to drop
scores.remove(grade_drop) #use to remove the lowest grade
mod_scores = scores #this will be the scores after the lowest one has been dropped



#print the results below

print('----------------Results----------------')
print(f'{"Lowest score:":<20} {grade_drop}')
print(f'{"Modified list:":<20} {mod_scores}')
print(f'{"Scores Average:":<20} {avg:.2f}')

# the grading scale below
if avg >= 90:
    print(f"{'Your grade is: ':<20} {'A'}")
else: 
    if avg >= 80:
        print(f"{'Your grade is: ':<20} {'B'}")
    else:
        if avg >= 70:
            print(f"{'Your grade is: ':<20} {'C'}")
        else:
            if avg >= 60:
                print(f"{'Your grade is: ':<20} {'D'}")
            else:
                if avg < 60:
                    print(f"{'Your grade is: ':<20} {'F'}")
print('---------------------------------------')




