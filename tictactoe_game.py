
class TicTacToeGame:
    def __init__(self, player1, player2):
        self.board = [[" " for i in range(3)] for j in range(3)]
        self.player_mapping = {player1: "x", player2: "o"}
        self.turn = "x"

    def can_make_move(self, player, x, y):
        return self.board[y][x] == " " and self.turn == self.player_mapping[player]

    def make_move(self, player, x, y):
        self.board[y][x] = self.player_mapping[player]
        return True

    def calc_game_status(self):
        pass