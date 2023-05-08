import queue

from Board import Board, SquareIcon, Move


# TODO: Implement evaluation function

def _backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


class Solver:
    def __init__(self, depth_limit):
        self.depth_limit = depth_limit
        self.game_tree = {}

    def solve(self, board, player, search_method):
        if search_method == "MM":
            search_method = self._mini_max
        elif search_method == "AB":
            search_method = self._alpha_beta
        else:
            print(f"{search_method} is not a known search method")
        if board not in self.game_tree:
            self.game_tree = self._get_game_tree(board, player)
            print("creating new game tree")
        return self._mini_max(board, player)

    def _get_game_tree(self, board, player):
        game_tree = {}
        depth = 0
        q = queue.Queue()
        q.put(board)
        game_tree[board] = []

        while not q.empty():
            vertex = q.get()
            if vertex.depth == self.depth_limit:
                break
            if depth < vertex.depth:
                depth = vertex.depth
            for move in vertex.get_possible_moves(player):
                move.depth = depth + 1
                if game_tree[vertex]:
                    game_tree[vertex].append(move)
                else:
                    game_tree[vertex] = [move]
        return game_tree

        # parent = {}
        #
        # for move in board.get_possible_moves(player):
        #     new_board = board.object_move(move)
        #     parent[new_board] = board
        #     search = search_method(new_board, player, 0, parent)
        #     score = search[0]
        #     parent = search[1]
        #     if player.is_maximizing() and score > 0:
        #         break
        #     elif not player.is_maximizing() and score < 0:
        #         break
        # return move, _backtrace(parent, move,

    # def _mini_max(game_tree, root: Board, player: SquareIcon, parent):
    #     if root.is_full():  # is terminal node
    #         return -1 if current_player.is_maximizing() else 1
    #
    #     if game_tree[root] is None:  # is leaf node
    #         return evaluate(board, current_player.is_maximizing())
    #
    #     return (max if current_player.is_maximizing() else min)([
    #         _mini_max(game_tree, next_move, current_player.opposite()) for next_move in
    #         game_tree[root]
    #     ])

    def _mini_max(self, root: Board, current_player: SquareIcon):
        if root.is_full():  # is terminal node
            return -1 if current_player.is_maximizing() else 1

        if root not in self.game_tree:  # is leaf node
            return self.evaluate(root, current_player.is_maximizing())

        scores = []
        for next_move in self.game_tree[root]:
            next_move.set_score(self._mini_max(next_move, current_player.opposite()))
            scores.append(next_move)

        return (max if current_player.is_maximizing() else min)(scores)

    def _alpha_beta(self, board: Board, current_move: SquareIcon):
        print(board)

    def evaluate(self, board, is_maximizing):
        return 0.99 if is_maximizing else -0.99
