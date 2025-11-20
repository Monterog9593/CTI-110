import turtle          
win = turtle.Screen()  
t = turtle.Turtle()

# add some display options
t.pensize(3)            # increase pensize (takes integer)
t.pencolor("green")     # set pencolor (takes string)
t.shape("turtle")

#commands from here to the last line can be replaced 
side_length = 100;
t.forward(side_length)          
t.left(90)            
t.forward(side_length)
t.left(90)
t.forward(side_length)
t.left(90)
t.forward(side_length)

# end commands
win.mainloop()             # Wait for user to close window
