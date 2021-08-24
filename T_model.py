######################################
# The logic of the "Tik-Tac-Toe" game
######################################
class Board:
    """
    Defines new and empty game board.
    """

    # Constants
    MAT_SIZE = 3
    X = 1
    O = -1
    EMPTY = 0
    VICTORY = [-3, 3]

    def __init__(self):
        self.game_mat = [[self.EMPTY for _ in range(self.MAT_SIZE)] for _ in range(self.MAT_SIZE)]
        self.row_sum = 0
        self.col_sum = 0
        self.diagonal1_sum = 0
        self.diagonal2_sum = 0

    def check_victory(self):
        """
        Checks if one of the players won, by checking the sum of the rows, columns and diagonals.
        :return: The representation of the winner (as defined by the constants), or the representation of a tie (empty).
        """
        for i in range(self.MAT_SIZE):
            self.diagonal2_sum += self.game_mat[i][self.MAT_SIZE - (i + 1)]
        if self.diagonal2_sum in self.VICTORY:
            return ["d2", -1]

        for i in range(self.MAT_SIZE):
            for j in range(self.MAT_SIZE):
                self.row_sum += self.game_mat[i][j]
                self.col_sum += self.game_mat[j][i]
                if self.row_sum in self.VICTORY:
                    return ["r", i + 1]
                if self.col_sum in self.VICTORY:
                    return ["c", i + 1]
            self.diagonal1_sum += self.game_mat[i][i]
            if self.diagonal1_sum in self.VICTORY:
                return ["d1", -1]

            # Restart the counters, to count new summing.
            self.row_sum = 0
            self.col_sum = 0

        self.clear_sums()
        return  # If there are no winners yet.

    # def check_tie(self):

    def clear_sums(self):
        """
        Resets the sum counters.
        :return: None.
        """
        self.row_sum = 0
        self.col_sum = 0
        self.diagonal1_sum = 0
        self.diagonal2_sum = 0

    def reset(self):
        """
        Resets the board matrix. Specifically, turns all cells to be "0".
        :return: None.
        """
        self.game_mat = [[self.EMPTY for _ in range(self.MAT_SIZE)] for _ in range(self.MAT_SIZE)]
        self.clear_sums()

    def insert_value(self, value, location):
        """
        Inserts a given input value into a given loction on the board.
        :param value: 1 (X) or -1 (O).
        :param location: Array of two indexes - [row, col].
        :return: None.
        """
        self.game_mat[location[0]][location[1]] = value


class Score:

    X = 1
    O = -1

    def __init__(self):
        self.x_score = 0
        self.o_score = 0

    def get_x(self):
        return self.x_score

    def get_o(self):
        return self.o_score

    def add(self, player):
        if player == self.X:
            self.x_score += 1
        else:
            self.o_score += 1

    def reset(self):
        self.x_score = 0
        self.o_score = 0






