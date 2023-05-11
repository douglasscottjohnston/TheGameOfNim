import numpy as np
import copy

from enum import Enum
from pandas import DataFrame


class Board:

    def __init__(self, rows, columns, ai_move):
        """
        The board Class that can generate moves
        :param rows: The number of rows in the board
        :param columns: The number of columns in the board
        :param ai_move: The AI's move icon
        """
        self._rows = rows
        self._columns = columns
        self.previous_move = None
        self._score = 0
        self.depth = 0
        self._ai_move = ai_move
        self._state = [[Square(SquareIcon.EMPTY)] * self._columns for _ in range(self._rows)]

    def __getitem__(self, row):
        return self._state[row]

    def __str__(self):
        return str(DataFrame(np.matrix(self._state)))

    def __repr__(self):
        return "\n" + str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return self.get_score() < other.get_score()

    def __le__(self, other):
        return self.get_score() <= other.get_score()

    def __gt__(self, other):
        return self.get_score() > other.get_score()

    def __ge__(self, other):
        return self.get_score() >= other.get_score()

    def __hash__(self):
        return hash(str(self))

    def get_surrounding_squares(self, icon, row, column):
        """
        Gets an array of moves of all the surrounding squares of the passed index
        :param icon: The icon to pass to the Move constructor
        :param row: The row of the index to search from
        :param column: The column of the index to search from
        :return:
        """
        squares = [
            Move(icon, row - 1, column - 1) if row > 0 and column > 0 else None,  # top_left
            Move(icon, row - 1, column) if row > 0 else None,  # top
            Move(icon, row - 1, column + 1) if row > 0 and column < self._columns - 1 else None,  # top_right
            Move(icon, row, column - 1) if column > 0 else None,  # middle_left
            Move(icon, row, column + 1) if column < self._columns - 1 else None,  # middle_right
            Move(icon, row + 1, column - 1) if row < self._rows - 1 and column > 0 else None,  # bottom_left
            Move(icon, row + 1, column) if row < self._rows - 1 else None,  # bottom_middle
            Move(icon, row + 1, column + 1) if row < self._rows - 1 and
                                               column < self._columns - 1 else None,  # bottom_right
        ]

        return [square for square in squares if square is not None]

    def get_possible_moves(self, icon):
        """
        Returns an array of all possible moves that can be made from the current board
        :param icon: The icon to move with
        :return: An array of all possible moves that can be made from the current board
        """
        possible_moves = []
        for i in range(self._rows):
            for j in range(self._columns):
                move = self._move(icon, i, j)
                if move:
                    possible_moves.append(move)
        return possible_moves

    def _move(self, icon, row, column):
        if self[row][column].is_empty() and not self.is_full():
            move = copy.deepcopy(self)
            move.previous_move = Move(icon, row, column)
            move[row][column] = Square(icon)
            for square in move.get_surrounding_squares(icon, row, column):
                if square and move[square.row][square.column].is_empty():
                    move[square.row][square.column] = Square(SquareIcon.BLOCKED)
            return move
        else:
            return False

    def move(self, icon, row, column):
        """
        Handles player movement
        :param icon: The SquareIcon to preform the move
        :param row: The row of the move
        :param column: The column of the move
        :return: If the move is possible it returns a deep copy of the board with the move made or false otherwise
        """
        return self._move(icon, row, column)

    def object_move(self, move):
        """
        Preform a move using the Move object
        :param move: The move object
        :return: If the move is possible it returns a deep copy of the board with the move made or false otherwise
        """
        return self.move(move.icon, move.row, move.column)

    def x_move(self, row, column):
        return self._move(SquareIcon.XMOVE, row, column)

    def x_object_move(self, move):
        return self.x_move(move.row, move.column)

    def o_move(self, row, column):
        return self._move(SquareIcon.OMOVE, row, column)

    def o_object_move(self, move):
        return self.o_move(move.row, move.column)

    def get_rows(self):
        return self._rows

    def get_columns(self):
        return self._columns

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score

    def is_ai_turn(self, icon):
        return icon == self._ai_move

    def get_ai_move(self):
        return self._ai_move

    def get_num_empty_squares(self):
        empty_squares = 0
        for i in range(0, self._rows):
            for j in range(0, self._columns):
                if self[i][j].is_empty():
                    empty_squares += 1
        return empty_squares

    def is_full(self):
        for i in range(0, self._rows):
            for j in range(0, self._columns):
                if self[i][j].is_empty():
                    return False
        return True


class Move:
    def __init__(self, icon, row, column):
        """
        The move object
        :param icon: The icon for the move
        :param row: The row of the move
        :param column: The column of the move
        """
        self.valid = True
        if row < 0:
            print("row must be positive")
            self.valid = False
        if column < 0:
            print("column must be positive")
            self.valid = False
        self.row = row
        self.column = column
        self.icon = icon


class Square:
    def __init__(self, icon):
        """
        The square object that represents a square in the board
        :param icon: The icon to store in the square
        """
        self.icon = icon

    def __repr__(self):
        return self.icon.value

    def __str__(self):
        return self.icon.value

    def __copy__(self):
        return Square(self.icon)

    def is_empty(self):
        return self.icon == SquareIcon.EMPTY


class SquareIcon(Enum):
    """
    Enum used to represent icons in squares
    """
    EMPTY = "-"
    BLOCKED = "/"
    XMOVE = "X"
    OMOVE = "O"

    def __str__(self):
        return str(self.value)

    def opposite(self):
        return self.XMOVE if self == self.OMOVE else self.OMOVE

    def is_maximizing(self):
        return self == self.OMOVE
