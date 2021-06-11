from copy import deepcopy

directions = (UP_DIR, DOWN_DIR, LEFT_DIR, RIGHT_DIR) = ((-1, 0), (1, 0), (0, -1), (0, 1))
dirIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class Grid:
    def __init__(self, size = 4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    def copying(self):
        temp = Grid()
        temp.map = deepcopy(self.map)
        temp.size = self.size
        return temp

    def insertTile(self, pos, value):
        self.setCellValue(pos, value)

    def setCellValue(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def getEmptyCells(self):
        cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == 0:
                    cells.append((i,j))
        return cells

    def getHighestTile(self):
        highestValueCell = 0
        for i in range(self.size):
            for j in range(self.size):
                highestValueCell = max(highestValueCell, self.map[i][j])
        return highestValueCell

    def checkInsertion(self, pos):
        return self.getCellValue(pos) == 0

    def move(self, dir):
        dir = int(dir)
        if dir == UP:
            return self.moveUpOrDown(False)
        if dir == DOWN:
            return self.moveUpOrDown(True)
        if dir == LEFT:
            return self.moveLeftOrRight(False)
        if dir == RIGHT:
            return self.moveLeftOrRight(True)

    def moveUpOrDown(self, down):
        r = range(self.size -1, -1, -1) if down else range(self.size)
        isMoved = False
        for j in range(self.size):
            cells = []
            for i in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)
            self.combine(cells)
            for i in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    isMoved = True
                self.map[i][j] = value
        return isMoved

    def moveLeftOrRight(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)
        isMoved = False
        for i in range(self.size):
            cells = []
            for j in r:
                cell = self.map[i][j]
                if cell != 0:
                    cells.append(cell)
            self.combine(cells)
            for j in r:
                value = cells.pop(0) if cells else 0
                if self.map[i][j] != value:
                    isMoved = True
                self.map[i][j] = value
        return isMoved

    def combine(self, cells):
        if len(cells) <= 1:
            return cells
        count = 0
        while count < len(cells) - 1:
            if cells[count] == cells[count+1]:
                cells[count] *= 2
                del cells[count+1]
            count += 1

    def checkIfMove(self, dirs = dirIndex):
        checkPossibleMoves = set(dirs)

        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y]:
                    for i in checkPossibleMoves:
                        possibleMove = directions[i]
                        adjValue = self.getCellValue((x + possibleMove[0], y + possibleMove[1]))
                        if adjValue == self.map[x][y] or adjValue == 0:
                            return True
                elif self.map[x][y] == 0:
                    return True
        return False

    def getPossibleMoves(self, dirs = dirIndex):
        possibleMoves = []
        for x in dirs:
            temp = self.copying()
            if temp.move(x):
                possibleMoves.append(x)
        return possibleMoves

    def crossBound(self, pos):
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    def getCellValue(self, pos):
        if not self.crossBound(pos):
            return self.map[pos[0]][pos[1]]
        else:
            return None

if __name__ == '__main__':
    g = Grid()
    g.map[0][0] = 2
    g.map[2][0] = 4
    while True:
        for i in g.map:
            print(i)
        print (g.getPossibleMoves())
        v = raw_input()
        g.move(v)
