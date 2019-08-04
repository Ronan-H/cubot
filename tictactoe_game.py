
class TicTacToeGame:
    def __init__(self, player1, player2):
        self.board = [[" " for i in range(3)] for j in range(3)]
        self.player_mapping = {player1: "x", player2: "o"}
        self.turn = "x"

    def can_make_move(self, player, x, y):
        return self.board[y][x] == " " and self.turn == self.player_mapping[player]

    def make_move(self, player, x, y):
        self.board[y][x] = self.player_mapping[player]
        self.turn = "x" if self.turn == "o" else "x"
        return True

    def calc_game_status(self):
        # rows
        lines = self.board
        # columns
        lines += [[self.board[i][j] for i in range(3)] for j in range(3)]
        # diagonals
        lines += [self.board[i][i] for i in range(3)]
        lines += [self.board[i][2 - i] for i in range(3)]

        for p in ["x", "o"]:
            if any(all(c == p for c in line) for line in lines):
                return p

        return False
