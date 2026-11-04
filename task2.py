import turtle
import math


def draw_tree(pen, length, level):
    if level == 0:
        return

    pen.forward(length)

    # Save the position and direction at the branch point.
    position = pen.position()
    heading = pen.heading()

    pen.left(35)
    draw_tree(pen, length / math.sqrt(2), level - 1)

    # Return to the branch point before drawing the other branch.
    pen.penup()
    pen.goto(position)
    pen.setheading(heading)
    pen.pendown()

    pen.right(35)
    draw_tree(pen, length / math.sqrt(2), level - 1)

    # Restore the branch point and original direction.
    pen.penup()
    pen.goto(position)
    pen.setheading(heading)
    pen.pendown()


def main():
    try:
        level = int(input("Enter recursion level (1–12): "))
    except ValueError:
        print("Please enter an integer.")
        return

    if not 1 <= level <= 12:
        print("Recursion level must be between 1 and 12.")
        return

    screen = turtle.Screen()
    screen.title("Pythagoras Tree")
    screen.setup(900, 800)
    screen.tracer(0)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.color("firebrick")

    pen.penup()
    pen.goto(0, -300)
    pen.setheading(90)
    pen.pendown()

    draw_tree(pen, 150, level)

    screen.update()
    screen.exitonclick()


if __name__ == "__main__":
    main()