import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import random
import pickle
import os

# File to store data
DATA_FILE = "tictactoe_data.pkl"

# Load persistent data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {"player_name": "", "score": 0, "history": []}

# Save persistent data
def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

# Check winner
def check_winner(board, player):
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in wins)

# Main App
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.data = load_data()

        if not self.data['player_name']:
            self.data['player_name'] = simpledialog.askstring("Player Name", "Enter your name:")
            save_data(self.data)

        self.score = self.data['score']
        self.history = self.data['history']
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()
        self.home_frame = tk.Frame(self.root)
        self.home_frame.pack(pady=50)

        tk.Label(self.home_frame, text=f"Welcome {self.data['player_name']}!", font=("Arial", 18)).pack()
        self.score_label = tk.Label(self.home_frame, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack(pady=10)

        tk.Button(self.home_frame, text="Start New Game", command=self.start_game).pack(pady=5)
        tk.Button(self.home_frame, text="Change Name", command=self.change_name).pack(pady=5)
        tk.Button(self.home_frame, text="View Game History", command=self.view_history).pack(pady=5)
        tk.Button(self.home_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def start_game(self):
        self.clear_screen()
        self.board = [""] * 9
        self.buttons = []
        self.current_player = "X"
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=30)

        for i in range(9):
            btn = tk.Button(self.game_frame, text="", width=5, height=2,
                            font=("Arial", 24), command=lambda i=i: self.user_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def user_move(self, index):
        if self.board[index] == "":
            self.board[index] = "X"
            self.buttons[index].config(text="X", state="disabled")
            if check_winner(self.board, "X"):
                self.end_game("win")
                return
            elif "" not in self.board:
                self.end_game("draw")
                return
            self.root.after(300, self.ai_move)

    def ai_move(self):
        move = self.get_best_move()
        if move is not None:
            self.board[move] = "O"
            self.buttons[move].config(text="O", state="disabled")
            if check_winner(self.board, "O"):
                self.end_game("lose")
            elif "" not in self.board:
                self.end_game("draw")

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(self.board, 0, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        if check_winner(board, "O"):
            return 1
        elif check_winner(board, "X"):
            return -1
        elif "" not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def end_game(self, result):
        msg = {"win": "You Won!", "lose": "You Lost!", "draw": "It's a Draw!"}
        if result == "win":
            self.score += 10
        elif result == "lose":
            self.score -= 10

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({"datetime": dt, "result": result})
        self.data['score'] = self.score
        self.data['history'] = self.history
        save_data(self.data)

        messagebox.showinfo("Game Over", msg[result])
        self.create_home_screen()

    def change_name(self):
        name = simpledialog.askstring("Change Name", "Enter new name:")
        if name:
            self.data['player_name'] = name
            save_data(self.data)
            self.create_home_screen()

    def view_history(self):
        self.clear_screen()
        hist_frame = tk.Frame(self.root)
        hist_frame.pack(pady=20)
        tk.Label(hist_frame, text="Game History", font=("Arial", 16)).pack()
        if not self.history:
            tk.Label(hist_frame, text="No games played yet.").pack()
        else:
            for entry in self.history:
                tk.Label(hist_frame, text=f"{entry['datetime']} - {entry['result'].capitalize()}").pack()
        tk.Button(hist_frame, text="Back", command=self.create_home_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
