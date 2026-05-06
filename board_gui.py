import tkinter as tk
from board import Board
from ai_agent import AlphaBetaAgent

SIZE = 9
CELL = 60
MARGIN = CELL


class GoGUI:
    def __init__(self):
        self.game = Board()
        self.ai = AlphaBetaAgent(depth=2)
        self.root = tk.Tk()
        self.root.title("Go AI - AlphaBeta")

        canvas_size = 2 * MARGIN + (SIZE - 1) * CELL
        self.turn_label = tk.Label(self.root, text="Black's Turn", font=("Arial", 14))
        self.turn_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size, bg="beige")
        self.canvas.pack()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Pass", command=self.on_pass).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="AI Move (Current Side)", command=self.run_ai).pack(side=tk.LEFT, padx=5)

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def run_ai(self):
        is_maximizing = True if self.game.current_player == 1 else False
        _, move = self.ai.search(self.game, self.ai.depth, float('-inf'), float('inf'), is_maximizing)

        if move:
            self.game.place(move[0], move[1])
            self.draw_board()
            self._update_banner()
        else:
            self.on_pass()

    def _update_banner(self):
        color = "Black" if self.game.current_player == 1 else "White"
        self.turn_label.config(text=f"{color}'s Turn")

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
                if piece == 0: continue
                x, y = MARGIN + col * CELL, MARGIN + row * CELL
                color = "black" if piece == 1 else "white"
                self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=color)

    def on_click(self, event):
        col = round((event.x - MARGIN) / CELL)
        row = round((event.y - MARGIN) / CELL)
        if 0 <= row < SIZE and 0 <= col < SIZE:
            if self.game.place(row, col):
                self.draw_board()
                self._update_banner()

    def on_pass(self):
        self.game.skip()
        self._update_banner()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GoGUI()
    app.run()