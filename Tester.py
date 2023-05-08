import sys

from Board import Board, SquareIcon, Move
from Solver import solve

players = {1: SquareIcon.OMOVE, 2: SquareIcon.XMOVE}


def main():
    ai_move = int(sys.argv[1])
    search_method = sys.argv[2]
    size = sys.argv[3]
    rows = int(size.split("*")[0])
    columns = int(size.split("*")[1])
    ai_move = players[ai_move]
    board = Board(rows, columns, ai_move)
    human_move = ai_move.opposite()
    current_move = players[1]
    print(board)

    while board.empty_squares > 0:
        if board.is_ai_turn(current_move):
            move = solve(board, ai_move, search_method)
            board = board.object_move(move)
            print(board)
            print(f"{ai_move} makes a move: {move.row}/{move.column}")
        else:
            move = input("Enter your move(row,column): ").split(",")
            move = Move(human_move, int(move[0]), int(move[1]))
            board = board.object_move(move)
            if move:
                print(board)
                print(f"{human_move} makes a move: {move.row}/{move.column}")
            else:
                print(
                    f"invalid move: {move.row}, {move.column}\nrow must be between 0 and {board.get_rows() - 1}\ncolumn must be between 0 and {board.get_columns() - 1}")
                break
        current_move = current_move.opposite()
    print(board)
    print(f"{current_move} is out of moves and loses")


if __name__ == "__main__":
    main()
