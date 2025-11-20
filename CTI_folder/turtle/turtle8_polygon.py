import turtle          
win = turtle.Screen()  
t = turtle.Turtle()

# add some display options
t.pensize(4)            # increase pensize (takes integer)
t.pencolor("red")     # set pencolor (takes string)
t.shape("turtle")

#commands from here to the last line can be replaced

# draw a N sided polygon
numSides = int(input("How many sides in the polygon?"))
               
angle = 360 / numSides
sides = range(numSides)
# distance = 300 / numSides # try different values 
distance = 80
               
for i in sides:
    t.forward(distance)
    t.left(angle)


# end commands
win.mainloop()             # Wait for user to close window
