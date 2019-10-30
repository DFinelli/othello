"""
Dan Finelli
CS 5001
HW6
November 10, 2018
"""
import turtle
   
def draw_circle(turn, x, y, board, square, circle):
    '''
    name: draw_circle
    input: 1 string, 5 integers: string is the current player turn. x&y coords
    of click, board size (#x#), square drawing size, circle drawing radius are
    the 5 int inputs
    returns: nothing
    does: draws a circle at the (x,y) clicked location. Color is based on turn
    '''
    
    radius = 20
    turtle.setpos(0,0)
    center_x = (x / abs(x)) * (((abs(x) // square) * square) + (square/2))
    if int(y / abs(y)) == -1:
        center_y = ((y / abs(y)) * ((abs(y) // square) * square)) - square +\
                   ((square - (circle * 2)) / 2)
    else:
        center_y = ((y / abs(y)) * ((abs(y) // square) * square)) +\
                   ((square - (circle * 2)) / 2)

    turtle.penup()
    turtle.setpos(center_x, center_y)
    #print(center_x, center_y)
    if turn == "P1":
        turtle.color("black")
    elif turn == "P2":
        turtle.color("white")
    turtle.pendown()
    turtle.begin_fill()
    turtle.circle(circle)
    turtle.end_fill()
    turtle.penup()

def draw_board(board, square, circle):
    '''
        name: draw_board
        input: 3 ints: board size (#x#), square size to draw, & circle
        size to draw)
        returns: nothing
        does: draws an board with a green background
    '''
    turtle.speed(75)
    turtle.setup(board * square + square, board * square + square)
    turtle.screensize(board * square, board * square)
    turtle.bgcolor('white')

    # Create the turtle to draw the board
    othello = turtle.Turtle()
    othello.penup()
    othello.speed(0)
    othello.hideturtle()

    # Line color is black, fill color is green
    othello.color("black", "forest green")
    
    # Move the turtle to the upper left corner
    corner = -board * square / 2
    othello.setposition(corner, corner)
  
    # Draw the green background
    othello.begin_fill()
    for i in range(4):
        othello.pendown()
        othello.forward(square * board)
        othello.left(90)
    othello.end_fill()

    # Draw the horizontal nes
    for i in range(board + 1):
        othello.setposition(corner, square * i + corner)
        draw_lines(othello, board, square, circle)

    # Draw the vertical lines
    othello.left(90)
    for i in range(board + 1):
        othello.setposition(square * i + corner, corner)
        draw_lines(othello, board, square, circle)

    # Draw beginning pieces

    turtle.penup()
    turtle.setpos(0, 0)
    
    # Calculates beginning coord locations of the 4 pieces in a nested list
    #[[NW B], [SE W], [SW W], [SE B]]  ---> NW=NorthWest, etc.
    begin_coords = [[-1 * (square / 2), (square - (circle * 2)) / 2, "black"],
                    [square / 2, (square - (circle * 2)) / 2, "white"],
                    [-1 * (square / 2), -1 * (square - ((square -\
                    (circle * 2)) / 2)), "white"],
                    [square / 2, -1 * (square - ((square - (circle * 2)) / 2)),\
                     "black"]]
    # Iterates through nested list to draw beginning circles at coordinate value
    for coords in range(len(begin_coords)):
        turtle.setpos(begin_coords[coords][0], begin_coords[coords][1])
        turtle.color(begin_coords[coords][2])
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(circle)
        turtle.end_fill()
        turtle.penup()

def draw_lines(othello, board, square, circle):
    '''
    name: draw_lines
    input: 1 string, 3 int. string is the turtle object. 3 ints are the board
    size (#x#), square drawing size, and circle radius
    returns: nothing
    does: draws a grid of lines over the green board background
    '''
    othello.pendown()
    othello.forward(square * board)
    othello.penup()

