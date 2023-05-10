import sys

from Board import Board, SquareIcon, Move
from Solver import Solver

players = {1: SquareIcon.OMOVE, 2: SquareIcon.XMOVE}
move_to_players = {SquareIcon.OMOVE: 1, SquareIcon.XMOVE: 2}
search_method_strings = {"MM": "Minimax", "AB": "Minimax with AB pruning"}
GAME_TREE_DEPTH = 3


def append_to_readme(board, solver, search_method):
    file = open("readme.txt", "a")
    file.write(f"*** {board.get_rows} x {board.get_columns()} Board ***\n\n")
    file.write(f"AI is player {move_to_players[board.get_ai_move()]}:\n")
    file.write(search_method_strings[search_method] + "\n")
    file.write(f"Nodes expanded: {solver.nodes_expanded}\n")
    file.write(f"Depth level {GAME_TREE_DEPTH}")


def main():
    """
    Handles arguments and the main game loop
    :return: None
    """
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
    solver = Solver(GAME_TREE_DEPTH)

    while not board.is_full():  # game loop
        if board.is_ai_turn(current_move):  # handles ai moves
            board = solver.solve(board, ai_move, search_method)
            print(board)
            move = board.previous_move
            print(f"{ai_move} makes a move: {move.row}/{move.column}")
        else:  # handles human moves
            move = input("Enter your move(row,column): ").split(",")
            # input validation
            if int(move[0]) >= board.get_rows():
                print(f"row must be between 0 and {board.get_rows() - 1}")
                continue
            if int(move[1]) >= board.get_columns():
                print(f"column must be between 0 and {board.get_columns() - 1}")
                continue
            move = Move(human_move, int(move[0]), int(move[1]))
            if not move.valid:
                continue
            new_board = board.object_move(move)
            if new_board:  # the move was possible!
                board = new_board
                print(board)
                print(f"{human_move} makes a move: {move.row}/{move.column}")
            else:  # that move isn't possible :(
                print(f"invalid move: {move.row}, {move.column}\n")
                continue
        current_move = current_move.opposite()  # alternate moves
    print(board)
    print(f"{current_move} is out of moves and loses")
    append_to_readme(board, solver, search_method)


if __name__ == "__main__":
    main()
