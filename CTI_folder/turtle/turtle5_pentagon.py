import turtle          
win = turtle.Screen()  
t = turtle.Turtle()

# add some display options
t.pensize(4)            # increase pensize (takes integer)
t.pencolor("orange")     # set pencolor (takes string)
t.shape("turtle")

#commands from here to the last line can be replaced
# pentagon, sides are 360 / 5 = 72 degrees
 
t.left(180)             # this time we'll draw it in a different direction

# draw the pentagon
t.forward(100)
t.left(72)
t.forward(100)
t.left(72)
t.forward(100)
t.left(72)
t.forward(100)
t.left(72)
t.forward(100)

# end commands
win.mainloop()             # Wait for user to close window
