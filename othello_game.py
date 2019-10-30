
from othello_classes import Board
from othello_module import draw_board

# Set global variables. Board is size of board (#x#). Square is the size of each
# each square to be drawn. Circle is radius of circle to be drawn.

BOARD = 4
SQUARE = 50
CIRCLE = 20

def main():

    # Instantiate an Othello board object from the Board() class imported
    # from othello_classes file given the constant variables
    my_board = Board(BOARD, SQUARE, CIRCLE)

    # Draw boards an Othello board using function from module according to
    # constant variables
    draw_board(BOARD, SQUARE, CIRCLE)

main()


