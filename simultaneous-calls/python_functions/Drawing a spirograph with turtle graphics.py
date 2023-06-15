import turtle

def draw_spirograph(radius, num_loops, rotation_angle):
    # Set up the turtle
    turtle.speed(0)
    turtle.bgcolor("black")
    turtle.pensize(1)
    turtle.color("yellow")

    # Draw the spirograph
    for _ in range(num_loops):
        turtle.circle(radius)
        turtle.right(rotation_angle)

    # Hide the turtle and display the window
    turtle.hideturtle()
    turtle.done()

# Example usage: draw a spirograph with a radius of 100, 60 loops, and a rotation angle of 6 degrees
draw_spirograph(100, 60, 6)