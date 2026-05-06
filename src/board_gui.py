import tkinter as tk
from board import Board

SIZE = 9
CELL = 60
MARGIN = CELL


class GoGUI:

    def __init__(self):
        self.game = Board()

        self.root = tk.Tk()
        self.root.title("Go Game")

        canvas_size = 2 * MARGIN + (SIZE - 1) * CELL

        self.turn_label = tk.Label(self.root, text="Black's Turn", font=("Arial", 14))
        self.turn_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size, bg="beige")
        self.canvas.pack()

        self.pass_button = tk.Button(self.root, text="Pass", command=self.on_pass)
        self.pass_button.pack(pady=5)

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def _update_banner(self):
        if self.game.current_player == 1:
            self.turn_label.config(text="Black's Turn")
        else:
            self.turn_label.config(text="White's Turn")

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(SIZE):
            x = MARGIN + i * CELL
            y = MARGIN + i * CELL
            self.canvas.create_line(MARGIN, y, MARGIN + (SIZE - 1) * CELL, y, width=2)
            self.canvas.create_line(x, MARGIN, x, MARGIN + (SIZE - 1) * CELL, width=2)

        for row in range(SIZE):
            for col in range(SIZE):
                piece = self.game.board[row][col]
                if piece == 0:
                    continue
                x = MARGIN + col * CELL
                y = MARGIN + row * CELL
                radius = CELL // 2 - 4
                color = "black" if piece == 1 else "white"
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def on_click(self, event):
        if self.game.game_over:
            return
        col = round((event.x - MARGIN) / CELL)
        row = round((event.y - MARGIN) / CELL)
        if not (0 <= row < SIZE and 0 <= col < SIZE):
            return
        old_board = [r[:] for r in self.game.board]
        self.game.place(row, col)
        if old_board != self.game.board:
            self.draw_board()
            self._update_banner()
        if self.game.game_over:
            self.show_winner()

    def on_pass(self):
        if self.game.game_over:
            return
        self.game.skip()
        self._update_banner()
        if self.game.game_over:
            self.show_winner()

    def show_winner(self):
        self.game.scoring()
        black = self.game.black_score
        white = self.game.white_score
        winner = "Black" if black > white else "White"

        top = tk.Toplevel(self.root)
        top.title("Game Over")
        tk.Label(top, text=f"Black: {black}   White: {white}", font=("Arial", 12)).pack(pady=20,padx=20)
        tk.Label(top, text=f"{winner} wins!", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(top, text="Close", command=top.destroy).pack(pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GoGUI()
    app.run()