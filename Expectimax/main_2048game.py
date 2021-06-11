from game_board import GameBoard
from ai import AI
from random import randint, seed
import numpy as np

dirs = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}
# python main_cli > output.txt

stepCount_256Arr = []
stepCount_512Arr = []
stepCount_1024Arr = []
stepCount_2048Arr = []
stepCount_4096Arr = []
gameMaxValues = []
totalGames = 50

class CLIRunner:
    def __init__(self):
        self.board = GameBoard()
        self.ai = AI()

        self.init_game()
        # self.print_board()

        self.run_game()

        self.over = False

    def init_game(self):
        self.insert_random_tile()
        self.insert_random_tile()


    def checkValue(self, param):
        elem_to_find = param
        return any(elem_to_find in sublist for sublist in self.board.grid)

    """
    Player tries to solve the game by merging the tiles together by choosing best move
    computer tries to insert random tiles at random location
    """
    def run_game(self):
        turn_count = 0
        step_count_256 = 0
        step_count_512 = 0
        step_count_1024 = 0
        step_count_2048 = 0
        step_count_4096 = 0
        while True:
            turn_count += 1
            move = self.ai.get_move(self.board)
            self.board.move(move)
            self.insert_random_tile()

            if step_count_256 == 0 and self.checkValue(256):
                step_count_256 = turn_count
            if step_count_512 == 0 and self.checkValue(512):
                step_count_512 = turn_count
            if step_count_1024 == 0 and self.checkValue(1024):
                step_count_1024 = turn_count
            if step_count_2048 == 0 and self.checkValue(2048):
                step_count_2048 = turn_count
            if step_count_4096 == 0 and self.checkValue(4096):
                step_count_4096 = turn_count

            if len(self.board.get_available_moves()) == 0:
                print("- Game Over (max tile / max score): " + str(self.board.get_max_tile()))
                gameMaxValues.append(self.board.get_max_tile())
                self.print_board()
                break

        stepCount_256Arr.append(step_count_256)
        stepCount_512Arr.append(step_count_512)
        stepCount_1024Arr.append(step_count_1024)
        stepCount_2048Arr.append(step_count_2048)
        stepCount_4096Arr.append(step_count_4096)

        if step_count_2048 != 0:
            print("- GAME WON -")
            print("- Step at which 1st 2048 occurred: ", step_count_2048)
            print("")
        else:
            print("- GAME LOST -")
            print("- NO 2048 -")
            print("")

    """
    Print the 4 X 4 board / grid
    """
    def print_board(self):
        for i in range(4):
            for j in range(4):
                print("%6d  " % self.board.grid[i][j], end="")
            print("")
        print("")

    """
    This function helps us to insert random 2 tiles at different locattions
    Initially value can be 2 or 4 
    """
    def insert_random_tile(self):
        if randint(0,99) < 100 * 0.9:
            value = 2
        else:
            value = 4

        cells = self.board.get_available_cells()
        pos = cells[randint(0, len(cells) - 1)] if cells else None

        if pos is None:
            return None
        else:
            self.board.insert_tile(pos, value)
            return pos


def saveToFile(fileName, arrayValue):
    a_file = open(fileName, "w")
    np.savetxt(a_file, arrayValue, delimiter=',')
    a_file.close()


if __name__ == '__main__':
    for i in range(totalGames):
        print("------ Game Number: ",i+1,"------")
        CLIRunner()

    saveToFile("step256.txt", stepCount_256Arr)
    saveToFile("step512.txt", stepCount_512Arr)
    saveToFile("step1024.txt", stepCount_1024Arr)
    saveToFile("step2048.txt", stepCount_2048Arr)
    # saveToFile("step4096.txt", stepCount_4096Arr)
    saveToFile("maxValuesList.txt", gameMaxValues)
