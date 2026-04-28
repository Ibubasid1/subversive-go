class Board:

    SIZE = 9

    def __init__(self):
        self.board = [[0]*Board.SIZE for _ in range(Board.SIZE)]
        self.moves = 0
        self.last_was_pass = False
        self.current_player = 1
        self.game_over = False

    def get_adj(self, row, col):
        adjacent = set()
        if row < 8:
            adjacent.add((row + 1, col))
        if row > 0:
            adjacent.add((row - 1, col))
        if col < 8:
            adjacent.add((row, col + 1))
        if col > 0:
            adjacent.add((row, col - 1))
        return adjacent
    
    def skip(self):
        if self.last_was_pass: #checks if opponent has already passed
            self.game_over = True #if opponent has, then the game should end
        else: #if the opponent hasn't, then the game continues 
            self.moves += 1
            self.last_was_pass = True

    def place(self, row, col): #uses a simply row and column to make the move
        #make a check to see whether the move is available
        if self.board[row][col] == 1 or self.board[row][col] == 2:
            print("Invalid move")
            return
        else:
            self.board[row][col] = self.current_player

        valid_move = False
        temp = self.get_adj(row, col)

        for element in temp:
            if self.count_liberties(element[0], element[1]) == 0 and self.board[element[0]][element[1]] != self.current_player:
                valid_move = True
                removable = self._traversal(element[0], element[1], self.board[element[0]][element[1]])
                for item in removable:
                    self.board[item[0]][item[1]] = 0
        
        if not valid_move:
            self.board[row][col] = 0
            print("Invalid move")
            return

        self.board[row][col] = self.current_player

        self.moves += 1

        self.current_player = 2 if self.current_player == 1 else 1

    def __str__(self):
        rows = []
        for row in self.board:
            rows.append("|".join(str(cell) for cell in row))
        return "\n".join(rows)

    def _traversal_helper(self, row, col, color, visited) -> set:
        visited.add((row, col))
        if (row + 1) < self.SIZE and self.board[row + 1][col] == color and (row + 1, col) not in visited:
            self._traversal_helper(row + 1, col, color, visited)
        if (row - 1) >= 0 and self.board[row - 1][col] == color and (row - 1, col) not in visited:
            self._traversal_helper(row - 1, col, color, visited)
        if (col + 1) < self.SIZE and self.board[row][col + 1] == color and (row, col + 1) not in visited:
            self._traversal_helper(row, col + 1, color, visited)
        if (col - 1) >= 0 and self.board[row][col - 1] == color and (row, col - 1) not in visited:
            self._traversal_helper(row, col - 1, color, visited)
        return visited

    #main traversal function, used so that the 'visited' set is not reset on every instance of recursion
    def _traversal(self, row, col, color) -> set:
        #checks for bounds and ensures color is the same as the piece currently in that position
        if(row >= 0 and row < 9 and col >= 0 and col < 9 and self.board[row][col] == color):
            visited = set()
            return self._traversal_helper(row, col, color, visited)
        return set()
    
    def count_liberties(self, row, col) -> int:
        visited = set()
        temp = self._traversal(row, col, self.board[row][col])
        for element in temp:
            r = element[0]
            c = element[1]
            #no need for a 'not in visited' check since if it was already in visited it would simply not be added again. sets hold unique values
            if r < 8 and self.board[r + 1][c] == 0:
                visited.add((r + 1, c))
            if r > 0 and self.board[r - 1][c] == 0:
                visited.add((r - 1, c))
            if c < 8 and self.board[r][c + 1] == 0:
                visited.add((r, c + 1))
            if c > 0 and self.board[r][c - 1] == 0:
                visited.add((r, c - 1))   
        return len(visited)             




def main():
    b = Board()
    b.place(1, 1)
    b.place(1, 2)
    b.place(2, 1)
    b.place(0, 1)
    b.place(0, 2)
    b.place(0, 0)
    b.place(3, 5)
    b.place(1, 0)
    empty = set()
    empty = b._traversal(0, 0, 2)
    print(b)
    for element in empty:
        print(element[0])
    print(", ".join(str(element) for element in empty))
    




    #if even number of moves, then black turn
    #if odd number of moves, then white turn
    #two possible moves, place or pass (maybe resign later)
    #let's call move 1 place and move 2 pass. If there are two consecutive move 2s, the game ends. 
    #however, the ai will likely not willingly pass. The random move will definitely not since that won't even be an option.
    #so, it's more likely that the game will end by the move limit we set, which will be 400

    #have created a new branch for this code, which will specifically be restricted to this file

if __name__ == "__main__":
    main()