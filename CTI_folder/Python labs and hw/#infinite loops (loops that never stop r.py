#infinite loops (loops that never stop running)

#score = 1

#while score > 0:
    #score = score * 2
    #print(score) # this causes a infinite loop and cause python to crash


# to end the loop rewrite as so

score = 1

while score < 10:
    score = score * 2
    print(score) 

# below is an example of an infinite loop
total = 10

while total != 3:
    print(total, end=" ")
    score = total / 2

