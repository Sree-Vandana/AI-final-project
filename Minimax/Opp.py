from random import randint

class Opp():
	def getMove(self, grid):
		cells = grid.getEmptyCells()
		if cells:
			return cells[randint(0, len(cells) - 1)]
		else:
			None
