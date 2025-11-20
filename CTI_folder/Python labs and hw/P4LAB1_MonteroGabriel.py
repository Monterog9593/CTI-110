#Gabriel Montero
#10/21/2025
#P4LAB1
#This program is a test to use turtle to draw a house
#Import the turtle program

import turtle

wn = turtle.Screen()
alex = turtle.Turtle()

#now make the turtle look like a turtle
alex.shape("turtle")

#adjusting speed of the turtle
alex.speed(1)

#screen background
screen = turtle.Screen()
screen.bgcolor("lightgreen")
#First write the code to draw the base (a square)
alex.color('blue')
#Written out code
alex.forward(50)
alex.left(90)
alex.forward(50)
alex.left(90)
alex.forward(50)
alex.left(90)
alex.forward(50)
alex.left(90)
alex.forward(50)
alex.left(90)

#same code but simplified
#for i in [0,1,2,3]:
#    alex.forward(50)
#    alex.left(90)

alex.penup()
alex.forward(50)     # This moves alex, but no line is drawn
alex.pendown()
#Next have it draw the roof(a triangle), make sure to code the roof to be filled with a color
alex.color('red')
alex.pensize(4)
alex.fillcolor('red')
alex.begin_fill()
alex.left(30)
alex.forward(50)
alex.left(120)
alex.forward(50)
alex.left(120)
alex.forward(50)
#for i in [0,1,2,]:
#    alex.forward(50)
#    alex.left(120)

#alex.penup()
#alex.forward(100)     # This moves alex, but no line is drawn
#alex.pendown()
alex.end_fill()
wn.mainloop() #prevents program closing