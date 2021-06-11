import Minimax
import AlphaBetaPrune
from Grid import Grid
import numpy as np
import Helper

class Player():
        def getMove(self, grid):
                copygrid = []
                for i in range(4):
                        copygrid.extend(grid.map[i])
                [child,moves] = Helper.getChildren(copygrid)
                maxpath = -np.inf
                direction = 0
                for i in range(len(child)):
                        c = child[i]
                        m = moves[i]
                        highest_value = -np.inf
                        maxdepth = 4
                        # highest_value = Minimax.calculate(c, maxdepth, False)
                        highest_value = AlphaBetaPrune.calculate(c, maxdepth, -np.inf, np.inf, False)
                        if m == 0 or m == 2:
                            highest_value += 10000
                        if highest_value > maxpath:
                            direction = m
                            maxpath = highest_value

                return direction

if __name__ == '__main__':
        agent = Player()
        g=Grid()
        g.map[0][0] = 2
        g.map[2][0] = 4
        while True:
                value = agent.getMove(g)
                g.move(value)



