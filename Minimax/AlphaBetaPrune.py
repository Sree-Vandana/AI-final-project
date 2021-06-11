import Helper
import numpy as np

def calculate(grid, depth, alpha, beta, isMax):
    if depth == 0:
        return Helper.heuristic(grid)
    if not Helper.isValidMove(grid):
        return Helper.heuristic(grid)
    if isMax:
        bestValue = -np.inf
        [child,moving] = Helper.getChildren(grid)
        for ch in child:
            bestValue = max(bestValue,calculate(ch,depth-1,alpha,beta,False))
            if bestValue >= beta:
                return bestValue
            alpha = max(alpha,bestValue)
        return bestValue
    else:
        cells = [i for i, x in enumerate(grid) if x == 0]
        child = []
        for c in cells:
            temp = list(grid)
            temp[c]=2
            child.append(temp)
            temp = list(grid)
            temp[c]=4
            child.append(temp)
        bestValue = np.inf
        for ch in child:
            bestValue = min(bestValue,calculate(ch,depth-1,alpha,beta,True))
            if bestValue <= alpha:
                return bestValue
            beta = min(beta,bestValue)
        return bestValue
