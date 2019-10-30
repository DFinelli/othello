
import turtle
import othello_module
import sys

class Board:
    '''
    Create a class, Board, that will create instances of an Othello board each
    4 attribute w/ defaults when instantiate (can be altered by class caller
    when instantiating. The remaining attributes are defaulted, must be changed
    by a method.

    attributes: board, square, circle, outside, clickable, turn, p1_points,
                p2_points, full_size, full_bool

    methods: create_database, clicked, determine_row, determine_col,
             check_inside, check_empty, check_legal, update_database,
             calculate_p1_points, calculate_p2_points, check_full,
             check_game_over, switch_players
    '''
    
    def __init__(self, board = 4, square = 50, circle = 20):
        '''
        name: __init__
        input: 3 optional ints -- Board size # is size of green board (#x#),
               square is size of squares in board, circle is radius of drawn
               circles, outside is the limit of the drawn board. & Self input
        returns: none
        does: instantiates a board object with its attributes and methods
        '''
        #Attributes related to board drawing. Outside is where the borders of
        # drawn board are. Clickable houses the turtle.onscreenclick fx.
        self.board = board
        self.square = square
        self.circle = circle
        self.outside = (self.board * self.square) / 2
        self.clickable = turtle.onscreenclick(self.clicked)

        # Attributes related to the player. Turn is player -- P1 (black) or
        # P2 (white). Each have their points begin at 0
        self.turn = "P1"
        self.p1_points = 0
        self.p2_points = 0

        # Attributes related to the database backend of the board. Full_size
        # is when board is full of player tiles, table is the nestled list of
        # P1/P2/empty tiles. Full_bool is a T/F checking if table is full
        self.full_size = self.board * self.board
        self.table = self.create_database()
        self.full_bool = False

    def create_database(self):
        '''
        name: create_database
        inputs: self
        returns: a nested list - the beginning database
        does: Creates the beginning database. An empty list is made. Then nests
              x num of lists, based on board size. Then puts x number of "E"s
              (e for empty), based on board size, into each nested list. Then
              places beginning P1/P2 tiles at 4 middle spots based on board size
        '''
        table = []
        for row in range(self.board):
            table.append([])
            for column in range(self.board):
                table[row].append("E")
                
        SE_start_pos = int(self.board / 2)
        table[SE_start_pos][SE_start_pos] = "P1"
        table[SE_start_pos][SE_start_pos - 1] = "P2"
        table[SE_start_pos - 1][SE_start_pos] = "P2"
        table[SE_start_pos -1][SE_start_pos - 1] = "P1"

        return table

    def clicked(self, x, y):
        '''
        name: clicked
        inputs: self, x & y -- xy coords from click location on turtle screen
        returns: bool: False OR program ends via sys.exit() and no return occurs
        does: serves as the argument for onscreenclick() turtle method. the x, y
              coords are passed through clicked function. several methods are
              called to faciliate the gameplay of Othello. If a click is valid
              gameplay happens, otherwise player keeps clicking. Gameplay ends
              if end game conditions are met and turtle/program are exited
        '''
        row = self.determine_row(y)
        col = self.determine_col(x)

        # Check if click legal. If not, player must keep clicking until legal.
        if self.check_legal(self.check_inside(row, col),\
                            self.check_empty(row, col)) == False:
            return False
        
        # If legal click, gameplay flow occurs
        else: 
            # update table with player's tile at the clicked spot
            self.update_database(self.turn, row, col)
            
            # draw circle with player's color at clicked spot
            othello_module.draw_circle(self.turn, x, y, self.board,\
                                       self.square, self.circle)
            
            # calculate points of both players
            self.calculate_p1_points()
            self.calculate_p2_points()

            # updates attribute if bord is full now. Then check if game is over.
            # If game over, program/turtle exit
            self.full_bool = self.check_full()
            self.check_game_over()

            # if game is not over, player turn attribute updated to next player
            # and next click will execute knowing (P1/P2 & White/Black)
            self.switch_player(self.turn)           
            
    def determine_row(self, y):
        '''
        name: determine_row
        input: self, int - y coordinate from click
        returns: int - corresponding row
        does: converts the y coordinate into the visual row seen on drawn board
              using int division. Row0,col0 is top left of board. if y is above
              the upper border, returns row as a negative to adjust for abs()
              used when calculating row and so valid click wil catch the (-)row
        '''
        if y > ((self.square * self.board) / 2):
            row = -1 * int(abs((y // self.square) - 1))
        else:
            row = int(abs((y // self.square) - 1))
        return row

    def determine_col(self, x):
        '''
        name: determine_col
        input: self, int - x coordinate from click
        returns: int - corresponding column
        does: converts the x coordinate into the visual row seen on drawn board
              using int division. Row0,col0 is top left of board.
        '''
        col = int((x // self.square) + (self.board / 2))
        return col

    def check_inside(self, row, col):
        '''
        name: check_inside
        input: self, 2 ints - the row, col of click location
        returns: bool - T if inside, F if outside
        does: checks the click's row,col and makes sure its inside the board
              based by seeing if each is greater than 0 less than the
              board's limits (size - 1)
        '''
        if row >= 0 and row <= (self.board - 1) and col >= 0 and col <=\
        (self.board - 1):
            return True
        else:
            return False

    def check_empty(self, row, col):
        '''
        name: check_empty
        input: self, 2 ints - row, col of click location
        returns: T or False
        does: checks if clicked location is empty in the database (E for empty).
              Also catches outside clicks row/col < 0 to make sure ex) row[-1]
              is not given to ex) row[3] if len(row) is 4. Also, handles index
              errors if row/col is outside and > len(board-1). Ex) len=4 and
              row[4] or row[5] --> would result in an index error
        '''
        try:
            if row < 0 or col < 0:
                return False
            if self.table[row][col] == "E":
                return True
            elif self.table[row][col] == "P1" or self.table[row][col] == "P2":
                return False
        except IndexError:
            return False

    def check_legal(self, inside, empty):
        '''
        name: check_legal
        input: self, 2 bools - if click is inside & if row/col data is empty
        returns: bool - T if move is legal, F if not legal
        does: Determines that a click is legal based on if both the click is
              inside the drawn board and if the database at row[col] is empty
        '''
        if inside == True and empty == True:
            return True
        else:
            return False

    def update_database(self, player, row, col):
        '''
        name: update_database
        input: self, string - current player(P1/P2), 2 ints - row/col of click
        returns: updated database table with legal click information,
                 returns False if IndexError
        does: stores a P1/P2 at the row/col location in the table database based
              off the valid click and current turn. Catches if click is out of
              bounds if < 0 or > (len - 1) of board.
        '''
        try:
            if row < 0 or col < 0:
                return False
            elif self.table[row][col] == "E":
                self.table[row][col] = player
            return self.table
        except IndexError:
            return False

    def calculate_p1_points(self):
        '''
        name: calculate_p1_points
        input: self
        returns: int, player 1 (black) points
        does: iterates through the nested lists and their values to sum
                 the P1's stored
        '''
        self.p1_points = 0

        try:
            
            for row_list in self.table:
                for col_value in row_list:
                    if col_value == "P1":
                        self.p1_points += 1
            return self.p1_points
        except IndexError:
            return False

    def calculate_p2_points(self):
        '''
        name:
        input: self,
        returns: int, player 2 (white) points
        does: iterates through the nested lists and their values to sum
              the P2's stored
        '''
        self.p2_points = 0

        try:
            for row_list in self.table:
                for col_value in row_list:
                    if col_value == "P2":
                        self.p2_points += 1
            return self.p2_points
        except IndexError:
            return False

    def check_full(self):
        '''
        name: check_full
        input: self
        returns: bool - T if board full, F if not
        does: sees if board is currently full by summing player 1 and player 2
              points and matching it will total possible tiles that could exist
              on the board (length x width)
        '''
        if self.p1_points + self.p2_points == self.full_size:
            return True
        else:
            return False
 
    def check_game_over(self):
        '''
        name: check_game_over
        input: self
        returns: bool, T if game over, F if not
        does: checks the full_bool attribute. if its true, game ends, click is
              turned off, turtle is exited, report to user the ending
              game over/winner or tie/player points. Then sys.exit the program. 
        '''
        if self.full_bool == True:
            self.clickable = turtle.onscreenclick(None)
            turtle.bye()
            print("Game over! Black had", self.p1_points,\
                  "points and White had", self.p2_points, "points.")
            if self.p1_points > self.p2_points:
                print("Black wins!")
            elif self.p2_points > self.p1_points:
                print("White wins!")
            else:
                print("Tie game!")
            sys.exit()

        else:
            return False
                
    def switch_player(self, player):
        '''
        name: switch_player
        input: self, string - the current player
        returns: string - the board's current turn
        does: updates the current board to the next player, based off who was
              previously clicking
        '''
        if self.turn == "P1":
            self.turn = "P2"
        elif self.turn =="P2":
            self.turn = "P1"
        return self.turn
