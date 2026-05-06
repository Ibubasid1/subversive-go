import copy


class Board:
    SIZE = 9

    def __init__(self):
        self.board = [[0] * Board.SIZE for _ in range(Board.SIZE)]
        self.moves = 0
        self.last_was_pass = False
        self.current_player = 1
        self.game_over = False
        self.black_score = 0
        self.white_score = 6.5

    def get_adj(self, row, col):
        adjacent = set()
        if row < 8: adjacent.add((row + 1, col))
        if row > 0: adjacent.add((row - 1, col))
        if col < 8: adjacent.add((row, col + 1))
        if col > 0: adjacent.add((row, col - 1))
        return adjacent

    def skip(self):
        if self.last_was_pass:
            self.game_over = True
        else:
            self.moves += 1
            self.last_was_pass = True
        if self.game_over:
            self._announce_winner()

    def place(self, row, col):
        if self.board[row][col] != 0:
            return False

        self.board[row][col] = self.current_player
        temp = self.get_adj(row, col)

        for element in temp:
            if self.count_liberties(element[0], element[1]) == 0 and self.board[element[0]][
                element[1]] != self.current_player:
                removable = self._traversal(element[0], element[1], self.board[element[0]][element[1]])
                for item in removable:
                    self.board[item[0]][item[1]] = 0

        if self.count_liberties(row, col) == 0:
            self.board[row][col] = 0
            return False

        self.last_was_pass = False
        self.moves += 1
        self.current_player = 2 if self.current_player == 1 else 1

        if self.moves >= 400: self.game_over = True
        return True

    def get_legal_moves(self):
        legal = []
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.board[r][c] == 0:
                    test_board = copy.deepcopy(self)
                    if test_board.place(r, c):
                        legal.append((r, c))
        return legal

    def _traversal_helper(self, row, col, color, visited) -> set:
        visited.add((row, col))
        for r, c in [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]:
            if 0 <= r < self.SIZE and 0 <= c < self.SIZE:
                if self.board[r][c] == color and (r, c) not in visited:
                    self._traversal_helper(r, c, color, visited)
        return visited

    def _traversal(self, row, col, color) -> set:
        if 0 <= row < 9 and 0 <= col < 9 and self.board[row][col] == color:
            return self._traversal_helper(row, col, color, set())
        return set()

    def count_liberties(self, row, col) -> int:
        liberties = set()
        group = self._traversal(row, col, self.board[row][col])
        for r, c in group:
            for adj_r, adj_c in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if 0 <= adj_r < 9 and 0 <= adj_c < 9 and self.board[adj_r][adj_c] == 0:
                    liberties.add((adj_r, adj_c))
        return len(liberties)

    def scoring(self):
        self.black_score = 0
        self.white_score = 6.5
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 1:
                    self.black_score += 1
                elif self.board[r][c] == 2:
                    self.white_score += 1

    def _announce_winner(self):
        self.scoring()
        print(f"P1: {self.black_score}, P2: {self.white_score}")