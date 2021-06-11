import numpy as np
import Helper

def calculate(grid, depth, isMax):
    if depth == 0:
        return Helper.heuristic(grid)
    if not Helper.isValidMove(grid):
        return Helper.heuristic(grid)
    if isMax:
        bestValue = -np.inf
        [child,moving] = Helper.getChildren(grid)
        for ch in child:
            bestValue = max(bestValue,calculate(ch,depth-1,False))
        return bestValue
    else:
        cells = [i for i, x in enumerate(grid) if x == 0]
        child = []
        bestValue = np.inf
        for c in cells:
            temp = list(grid)
            temp[c]=2
            child.append(temp)
            temp = list(grid)
            temp[c]=4
            child.append(temp)
        for ch in child:
            bestValue = min(bestValue,calculate(ch,depth-1,True))
        return bestValue
