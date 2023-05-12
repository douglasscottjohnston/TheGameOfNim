import queue

from Board import Board, SquareIcon, Move


def _is_odd(number):
    return number % 2 == 1


def _is_even(number):
    return number % 2 == 0


class Solver:
    def __init__(self, depth_limit):
        self.depth_limit = depth_limit
        self.game_tree = {}
        self.nodes_expanded = 0

    def solve(self, board, player, search_method):
        """
        The main function of the Solve class that handles when a new game tree should be made
        and what search method to use
        :param board: The game board
        :param player: The current player (the AI move usually)
        :param search_method: The search method to use (MM or AB)
        :return:
        """
        if search_method == "MM":
            search_method = self._mini_max
        elif search_method == "AB":
            search_method = self._alpha_beta
        else:
            print(f"{search_method} is not a known search method")
        if board not in self.game_tree or not self.game_tree[board]:  # Need to make a new game tree
            print("creating new game tree")
            self.game_tree = self._generate_game_tree(board, player)
        print("searching game tree")
        move = search_method(board, player)  # search the game tree
        return move

    def _generate_game_tree(self, root, player):
        """
        Creates a new game tree
        :param board: The root node of the game tree
        :param player: The current player (O or X)
        :return: A new game tree dict where game_tree[node] = array of all possible moves from that node
        """
        game_tree = {}
        depth = 0
        root.depth = 0
        root.previous_move = None
        q = queue.Queue()
        q.put(root)

        while not q.empty():
            vertex = q.get()
            if vertex.previous_move:
                player = vertex.previous_move.icon.opposite()
            if vertex not in game_tree:
                game_tree[vertex] = []
            if vertex.depth == self.depth_limit:
                continue
            if depth < vertex.depth:
                depth = vertex.depth
            for move in vertex.get_possible_moves(player):
                self.nodes_expanded += 1
                move.depth = depth + 1
                q.put(move)
                game_tree[vertex].append(move)
            # player = player.opposite() if vertex.previous_move is None else vertex.previous_move.icon.opposite()
        return game_tree

    def _mini_max(self, root: Board, current_player: SquareIcon):
        """
        The minimax search method
        :param root: The root node to search the game tree from
        :param current_player: The current player (X or O)
        :return: A board that represents the best next move to make
        """
        if root.is_full():  # is terminal node
            root.set_score(-1) if current_player.is_maximizing() else root.set_score(1)
            return root

        if root not in self.game_tree or not self.game_tree[root]:  # is leaf node
            root.set_score(self.evaluate(root, current_player.is_maximizing()))
            return root

        scores = []
        for next_move in self.game_tree[root]:
            next_move.set_score(self._mini_max(next_move, current_player.opposite()).get_score())
            scores.append(next_move)

        return (max if current_player.is_maximizing() else min)(scores)

    def _alpha_beta(self, root: Board, current_player: SquareIcon):
        """
        The alpha beta pruning search method
        :param board: The root node to search the game tree from
        :param current_move: The current player (X or O)
        :return: A board that represents the best next move to make
        """
        return self._alpha_beta_helper(root, current_player, -math.inf, math.inf)

        print(root)

    def _alpha_beta_helper(self, root: Board, current_player, alpha, beta):
        if root.is_full():  # is terminal node
            root.set_score(-1) if current_player.is_maximizing() else root.set_score(1)
            return root

        if root not in self.game_tree or not self.game_tree[root]:  # is leaf node
            root.set_score(self.evaluate(root, current_player.is_maximizing()))
            return root

        if current_player.is_maximizing():  # max level in game tree
            root.set_score(-math.inf)
            for child in self.game_tree[root]:
                self.nodes_expanded += 1
                root.set_score(
                    max(value, self._alpha_beta_helper(child, current_player.opposite(), alpha, beta))
                )
                if root.get_score() > beta:
                    break
                alpha = max(alpha, root.get_score())
            return root
        else:  # min level in game tree
            root.set_score(math.inf)
            for child in self.game_tree[root]:
                self.nodes_expanded += 1
                root.set_score(
                    min(value, self._alpha_beta_helper(child, current_player.opposite(), alpha, beta))
                )
                if root.get_score() < alpha:
                    break
                beta = min(beta, root.get_score())
            return root

    def evaluate(self, board, is_maximizing):
        move = board.previous_move
        squares_blocked = len(board.get_surrounding_squares(move.icon, move.row,
                                                            move.column)) + 1  # surrounding squares + the square the O or X is placed in
        empty_squares = board.get_num_empty_squares()

        if _is_odd(squares_blocked) and _is_odd(empty_squares):
            return -(squares_blocked / 10) if is_maximizing else squares_blocked / 10
        if _is_odd(squares_blocked) and _is_even(empty_squares):
            return squares_blocked / 10 if is_maximizing else -(squares_blocked / 10)
        if _is_even(squares_blocked) and _is_odd(empty_squares):
            return squares_blocked / 10 if is_maximizing else -(squares_blocked / 10)
        if _is_even(squares_blocked) and _is_even(empty_squares):
            return -(squares_blocked / 10) if is_maximizing else squares_blocked / 10