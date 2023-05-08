from Board import Board, SquareIcon, Move

# TODO: Implement game tree and evaluation function


DEPTH_LIMIT = 5

def solve(board, player, search_method):
    if search_method == "MM":
        search_method = _mini_max
    elif search_method == "AB":
        search_method = _alpha_beta
    else:
        print(f"{search_method} is not a known search method")
    return _get_best_move(board, player, search_method)


def _handle_output():
    return


def _get_best_move(board, player, search_method):
    for move in board.get_possible_moves(player):
        score = search_method(board.object_move(move), player, 0)
        if player.is_maximizing() and score > 0:
            break
        elif not player.is_maximizing() and score < 0:
            break
    return move


def _mini_max(board: Board, current_player: SquareIcon, depth):
    if board.is_full():
        return -1 if current_player.is_maximizing() else 1

    if depth == DEPTH_LIMIT:
        return evaluate(board, current_player.is_maximizing())

    return (max if current_player.is_maximizing() else min)([
        _mini_max(board.object_move(next_move), current_player.opposite(), depth + 1) for next_move in
        board.get_possible_moves(current_player)
    ])


def _alpha_beta(board: Board, current_move: SquareIcon):
    print(board)


def evaluate(board, is_maximizing):
    return 0.99 if is_maximizing else -0.99