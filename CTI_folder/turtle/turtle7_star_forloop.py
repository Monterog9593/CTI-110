import turtle          
win = turtle.Screen()  
t = turtle.Turtle()

# add some display options
t.pensize(4)            # increase pensize (takes integer)
t.pencolor("blue")     # set pencolor (takes string)
t.shape("turtle")

#commands from here to the last line can be replaced
# pentagon, sides are 360 / 5 = 72 degrees
 
t.left(180)             # this time we'll draw it in a different direction

# draw a star by adding a triangle on to each side
# this uses nested loops

for i in (1,2,3,4,5):
    # turn the other direction, so the triangle's on the outside
    for j in (1,2,3):
        t.forward(100)
        t.right(120)
    t.forward(100)
    t.left(72)


# end commands
win.mainloop()             # Wait for user to close window
