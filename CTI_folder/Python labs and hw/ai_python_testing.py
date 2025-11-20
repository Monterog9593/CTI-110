import turtle

def draw_square(pen):
    for _ in range(4):
        pen.forward(100)
        pen.right(90)

def draw_triangle(pen):
    for _ in range(3):
        pen.forward(100)
        pen.left(120)

def draw_circle(pen):
    pen.circle(50)

def draw_house(pen):
    # Draw square base
    pen.penup()
    pen.goto(-50, -50)  # Start at bottom-left corner
    pen.pendown()
    for _ in range(4):
        pen.forward(100)
        pen.left(90)

    # Draw roof
    pen.penup()
    pen.goto(-50, 50)  # Move to top-left corner of the square
    pen.pendown()
    pen.goto(0, 100)   # Peak of the roof
    pen.goto(50, 50)   # Top-right corner of the square


def draw_animal(pen):
    pen.penup()
    pen.goto(-20, -20)  # Body
    pen.pendown()
    pen.begin_fill()
    pen.circle(40)  # Body
    pen.end_fill()

    # Head
    pen.penup()
    pen.goto(-20, 40)
    pen.pendown()
    pen.begin_fill()
    pen.circle(20)
    pen.end_fill()

    # Ears
    pen.penup()
    pen.goto(-35, 60)
    pen.pendown()
    pen.begin_fill()
    pen.circle(5)
    pen.end_fill()

    pen.penup()
    pen.goto(-5, 60)
    pen.pendown()
    pen.begin_fill()
    pen.circle(5)
    pen.end_fill()

    # Eyes
    pen.penup()
    pen.goto(-28, 65)
    pen.pendown()
    pen.dot(3, "black")

    pen.penup()
    pen.goto(-12, 65)
    pen.pendown()
    pen.dot(3, "black")

    # Nose
    pen.penup()
    pen.goto(-20, 55)
    pen.pendown()
    pen.dot(4, "black")

    # Legs
    for x in [-35, -5]:
        pen.penup()
        pen.goto(x, -60)
        pen.setheading(-90)
        pen.pendown()
        pen.forward(20)

    # Tail
    pen.penup()
    pen.goto(20, 0)
    pen.setheading(45)
    pen.pendown()
    pen.forward(20)



# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")

# Create turtle
pen = turtle.Turtle()
pen.pensize(3)
pen.speed(2)

# Ask user for drawing type and color
drawing = screen.textinput("Choose Drawing", "Enter what to draw (square, triangle, circle, house, animal):").lower()
color = screen.textinput("Choose Color", "Enter a color (e.g., red, blue, green):").lower()
pen.color(color)

# Draw based on user input
if drawing == "square":
    draw_square(pen)
elif drawing == "triangle":
    draw_triangle(pen)
elif drawing == "circle":
    draw_circle(pen)
elif drawing == "house":
    draw_house(pen)
elif drawing == "animal":
    draw_animal(pen)
else:
    print("Unknown option. Try square, triangle, circle, house, or animal.")

# Finish
turtle.done()
