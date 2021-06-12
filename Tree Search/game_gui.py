import tkinter as tk
import random
import colors as c

class Game_gui(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048')

        self.base_matrix = tk.Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=400)
        self.base_matrix.grid(pady=(80, 0))
        self.create_GUI()
        
        
    def create_GUI(self):
        # make grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.base_matrix,
                    bg=c.EMPTY_CELL_COLOR,
                    width=200,
                    height=100)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.base_matrix, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        
        # make score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            score_frame,
            text="Game",
            font=c.SCORE_LABEL_FONT).grid(
            row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)
        
    def update_GUI(self, board,score):
            for i in range(4):
                for j in range(4):
                    cell_value = board[i][j]
                    if cell_value == 0:
                        self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                        self.cells[i][j]["number"].configure(
                            bg=c.EMPTY_CELL_COLOR, text="")
                    else:
                        self.cells[i][j]["frame"].configure(
                            bg=c.CELL_COLORS[cell_value])
                        self.cells[i][j]["number"].configure(
                            bg=c.CELL_COLORS[cell_value],
                            fg=c.CELL_NUMBER_COLORS[cell_value],
                            font=c.CELL_NUMBER_FONTS[cell_value],
                            text=str(cell_value))
            self.score_label.configure(text=score)
            self.update()
            
