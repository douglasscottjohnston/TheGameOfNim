import numpy as np
import copy

from enum import Enum
from pandas import DataFrame


class Board:
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._state = [[Square(SquareIcon.EMPTY)] * self._columns for _ in range(self._rows)]
        self._row_labels = [f"{i}" for i in range(self._rows)]
        self._column_labels = [f"{i}" for i in range(self._columns)]

    def __str__(self):
        return str(DataFrame(np.matrix(self._state), index=self._row_labels, columns=self._column_labels))

    def get_surrounding_squares(self, row, column):
        squares = {
            "top_left": Move(row - 1, column - 1),
            "top": Move(row - 1, column),
            "top_right": Move(row - 1, column + 1),
            "middle_left": Move(row, column - 1),
            "middle_right": Move(row, column + 1),
            "bottom_left": Move(row + 1, column - 1),
            "bottom_middle": Move(row + 1, column),
            "bottom_right": Move(row + 1, column + 1),
        }

        for item in squares.items():
            if item[1].row < 0 or item[1].column < 0 or item[1].row >= self._rows or item[1].column >= self._columns:
                squares[item[0]] = False

        return squares

    def get_possible_moves(self):
        possible_moves = []
        for i in range(self._rows):
            for j in range(self._columns):
                if self[i][j].is_empty():
                    possible_moves.append(Move(i, j))
        return possible_moves

    def _move(self, icon, row, column):
        if self[row][column].is_empty():
            move = copy.deepcopy(self)
            move[row][column] = Square(icon)
            for square in move.get_surrounding_squares(row, column).items():
                move[square.row][square.column] = Square(SquareIcon.BLOCKED)
            return move
        else:
            print(f"invalid move: row: {row}, column: {column}")
            return False

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

    def __getitem__(self, row):
        return self._state[row]


class Move:
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Square:
    def __init__(self, icon):
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
    EMPTY = "-"
    BLOCKED = "/"
    XMOVE = "X"
    OMOVE = "O"
