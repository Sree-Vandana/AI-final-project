import numpy as np

UP, DOWN, LEFT, RIGHT = range(4)


class AI():
    """
    To get best move of the player (maximize board value)
    @return best move number
    """

    def get_move(self, board):
        best_move, _ = self.maximize(board)
        return best_move

    """
    This function evaluates the board and returns the Utility value of the board
    Utility = SUM ( Sum of powers adjacent tiles values + absolute value of adjacent tiles + number of empty cells)
    """

    def eval_board(self, board, n_empty):
        grid = board.grid

        utility = 0
        smoothness = 0

        # for 4X4 grid --> consider taking columns and rows (0,1)(1,2)(2,3)
        big_t = np.sum(np.power(grid, 2))
        s_grid = np.sqrt(grid)
        smoothness -= np.sum(np.abs(s_grid[::, 0] - s_grid[::, 1]))
        smoothness -= np.sum(np.abs(s_grid[::, 1] - s_grid[::, 2]))
        smoothness -= np.sum(np.abs(s_grid[::, 2] - s_grid[::, 3]))
        smoothness -= np.sum(np.abs(s_grid[0, ::] - s_grid[1, ::]))
        smoothness -= np.sum(np.abs(s_grid[1, ::] - s_grid[2, ::]))
        smoothness -= np.sum(np.abs(s_grid[2, ::] - s_grid[3, ::]))

        empty_w = 100000
        smoothness_w = 3

        empty_u = n_empty * empty_w
        smooth_u = smoothness ** smoothness_w
        big_t_u = big_t

        utility += big_t
        utility += empty_u
        utility += smooth_u
        return (utility, empty_u, smooth_u, big_t_u)

    """
    this function calculates the maximum Utility function. and returns the best direction to take.
    steps invoved:
    1. get all available moves and game board
    2. calculate utility (see for maximum utility value), using chance
    """

    def maximize(self, board, depth=0):
        moves = board.get_available_moves()
        moves_boards = []

        for m in moves:
            m_board = board.clone()
            m_board.move(m)
            moves_boards.append((m, m_board))

        max_utility = (float('-inf'), 0, 0, 0)
        best_direction = None

        for mb in moves_boards:
            utility = self.chance(mb[1], depth + 1)  # chance of a board w.r.t depth of the tree

            if utility[0] >= max_utility[0]:  # choose the board with maximum Utility
                max_utility = utility
                best_direction = mb[0]

        return best_direction, max_utility  # return best direction to move in (UP, DOWN, RIGHT, LEFT)

    """
    adversary agents (minimizer) are not optimal, or their actions are based on chance.
    replaced minimizer nodes by chance nodes.
    Chance nodes take the average of all available utilities giving us the ‘expected utility’.
    This function Calculate chance based on current board grid and its depth 
    Steps Involve:
    1. get all available cells (Array),and calculate number of empty cells
    2. calculate utility value by evaluating the board or calculate maximum utility

    """

    def chance(self, board, depth=0):
        empty_cells = board.get_available_cells()
        n_empty = len(empty_cells)

        if n_empty >= 6 and depth >= 3:
            return self.eval_board(board, n_empty)

        if n_empty >= 0 and depth >= 5:
            return self.eval_board(board, n_empty)

        if n_empty == 0:
            _, utility = self.maximize(board, depth + 1)
            return utility

        possible_tiles = []

        chance_2 = (.9 * (1 / n_empty))
        chance_4 = (.1 * (1 / n_empty))

        for empty_cell in empty_cells:
            possible_tiles.append((empty_cell, 2, chance_2))
            possible_tiles.append((empty_cell, 4, chance_4))

        utility_sum = [0, 0, 0, 0]

        for t in possible_tiles:
            t_board = board.clone()
            t_board.insert_tile(t[0], t[1])
            _, utility = self.maximize(t_board, depth + 1)

            for i in range(4):
                utility_sum[i] += utility[i] * t[2]

        return tuple(utility_sum)
