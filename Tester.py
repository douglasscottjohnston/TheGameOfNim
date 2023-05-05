import sys

from Board import Board


def main():
    player = int(sys.argv[1])
    search_method = sys.argv[2]
    size = sys.argv[3]
    players = {1: lambda b, row, column: b.o_move(row, column), 2: lambda b, row, column: b.o_move(row, column)}
    ai_move = players[player]
    rows = int(size.split("*")[0])
    columns = int(size.split("*")[1])
    board = Board(rows, columns)
    print(board)
    move = ai_move(board, 1, 1)
    print(move)
    print(board)
    print(ai_move(move, 1, 5))


if __name__ == "__main__":
    main()
