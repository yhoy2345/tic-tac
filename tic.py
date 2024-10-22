import tkinter as tk
import math

class tic:
    def __init__(self, master):
        self.master = master
        self.master.title('Tic Tac Toe')
        self.master.geometry('320x380') # tamaño
        self.master.config(bg='black')  # fondo negro
        self.board = [' ' for _ in range(9)]  # tablero vacío
        self.current_player = 'X'  # comienza como X
        self.buttons = []
        self.game_mode = None

        # menú de selección de modo
        self.menu_frame = tk.Frame(self.master, bg='black')  # marco del menú
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Tic Tac Toe", font=('Arial', 20, 'bold'), fg='lightblue', bg='black').pack(pady=20) # titulo

        tk.Button(self.menu_frame, text="Jugar contra la IA", font=('Arial', 15,'bold'), command=self.start_vs_ai, bg='black', fg='pink').pack(pady=10) # opcion 1
        tk.Button(self.menu_frame, text="Jugadores locales", font=('Arial', 15, 'bold'), command=self.start_local_game, bg='black', fg='pink').pack(pady=10) # opcion 2

        # frame del tablero
        self.board_frame = tk.Frame(self.master, bg='black')  # marco en negro

    # iniciar el juego contra la IA
    def start_vs_ai(self):
        self.game_mode = 'AI'
        self.start_game()

    # iniciar el juego jugadores locales
    def start_local_game(self):
        self.game_mode = 'LOCAL'
        self.start_game()

    # inicializar el tablero del juego
    def start_game(self):
        self.menu_frame.pack_forget()  # ocultar menú
        self.board_frame.pack()  # mostrartablero

        for i in range(9):
            button = tk.Button(self.board_frame, text=' ', font=('Arial', 20), width=5, height=2,
                               bg='gray', command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    # movimiento del jugador
    def make_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.end_game(f'{self.current_player} ha ganado!!!!!')
            elif ' ' not in self.board:
                self.end_game('empate :P')
            else:
                if self.game_mode == 'LOCAL':
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                elif self.game_mode == 'AI' and self.current_player == 'X':
                    self.current_player = 'O'
                    self.ai_move()

    # movimiento de la IA
    def ai_move(self):
        best_score = -math.inf
        best_move = None

        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i

        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O')

        if self.check_winner('O'):
            self.end_game('La IA ha ganado:(')
        elif ' ' not in self.board:
            self.end_game('empate :P')
        else:
            self.current_player = 'X'

    # algoritmo Minimax
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('X'):
            return -1
        elif self.check_winner('O'):
            return 1
        elif ' ' not in board:
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    # verificarun ganador
    def check_winner(self, player):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == player:
                return True
        return False

    # terminar el juego y mostrar el mensaje del ganador
    def end_game(self, message):
        for button in self.buttons:
            button.config(state='disabled')
        label = tk.Label(self.master, text=message, font=('Arial', 20), bg='lightblue', fg='black')
        label.pack(pady=20)

# iniciar el juego
root = tk.Tk()
game = tic(root)
root.mainloop()
