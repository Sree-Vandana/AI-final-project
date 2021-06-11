from Grid import Grid
from Opp import Opp
from Player import Player
from random import randint
import time
import matplotlib.pyplot as plt
import numpy

initialTiles = 2
(Agent, Opponent) = (0, 1)
possibleDirections = {0:"UP", 1:'DOWN', 2:'LEFT', 3:'RIGHT'}
timeLimit = 1
prob = 0.9
max_tiles_array = []


class Game2048:
	def __init__(self, size = 4):
		self.grid = Grid(size)
		self.possibleTileValue = [2, 4]
		self.prob = prob
		self.initialTiles = initialTiles
		self.opponent = None
		self.agent = None
		self.end = False

	def setAgent(self, agent):
		self.agent = agent

	def setOpponent(self, opponent):
		self.opponent = opponent

	def setClock(self, time):
		if time - self.prevTime > timeLimit + 0.1:
			self.end = True
		else:
			self.prevTime = time

	def isGameCompleted(self):
		return not self.grid.checkIfMove()

	def insertRandonTile(self):
		tile = self.getNextTile()
		cells = self.grid.getEmptyCells()
		cell = cells[randint(0, len(cells) - 1)]
		self.grid.setCellValue(cell, tile)

	def getNextTile(self):
		if randint(0,99) < 100 * self.prob:
			return self.possibleTileValue[0]
		else:
			return self.possibleTileValue[1];

	def start(self):
		for i in range(self.initialTiles):
			self.insertRandonTile()

		self.Display(self.grid)

		turn = Agent
		highestTile = 0

		self.prevTime = time.perf_counter()

		while not self.isGameCompleted() and not self.end:
			temp = self.grid.copying()
			move = None

			if turn == Agent:
				print("Agent is playing")
				move = self.agent.getMove(temp)

				if move != None and move >= 0 and move < 4:
					if self.grid.checkIfMove([move]):
						self.grid.move(move)
						highestTile = self.grid.getHighestTile()
					else:
						print("Wrong Move")
						self.end = True
				else:
					print("Wrong Move - 1")
					self.end = True
			else:
				print("Opponent is playing")
				move = self.opponent.getMove(temp)
				if move and self.grid.checkInsertion(move):
					self.grid.setCellValue(move, self.getNextTile())
				else:
					print("Wrong move")
					self.end = True

			if not self.end:
				self.Display(self.grid)
			self.setClock(time.perf_counter())
			turn = 1 - turn
		max_tiles_array.append(highestTile)
		print("Highest Score for this game:",highestTile)

	def Display(self, grid):
		for i in range(grid.size):
			for j in range(grid.size):
				print("%6d  " % grid.map[i][j], end="")
			print ("")
		print ("")
		print ("")



def main():
	game = Game2048()
	agent  	= Player()
	opponent  = Opp()
	game.setAgent(agent)
	game.setOpponent(opponent)
	game.start()


if __name__ == '__main__':
	numiterations = 50
	for i in range(numiterations):
		print("--------------------------Iteration :", i + 1, "--------------------------------------")
		main()
	powersOf2 = [32, 64, 128, 256, 512, 1024, 2048]
	y = []
	mylabels = []
	print("Max tiles array", max_tiles_array)
	for i in range(len(powersOf2)):
		if (max_tiles_array.count(powersOf2[i]) != 0):
			y.append(max_tiles_array.count(powersOf2[i]))
			mylabels.append(str(powersOf2[i]) +'\n' + str((max_tiles_array.count(powersOf2[i]) / numiterations) * 100)+"%")
	result = numpy.array(y)
	print('Result', result)
	print('Labels', mylabels)
	print("Percentage of 32's", (max_tiles_array.count(32) / numiterations) * 100)
	print("Percentage of 64's", (max_tiles_array.count(64) / numiterations) * 100)
	print("Percentage of 128's", (max_tiles_array.count(128) / numiterations) * 100)
	print("Percentage of 256's", (max_tiles_array.count(256) / numiterations) * 100)
	print("Percentage of 512's", (max_tiles_array.count(512) / numiterations) * 100)
	print("Percentage of 1024's", (max_tiles_array.count(1024) / numiterations) * 100)
	print("Percentage of 2048's", (max_tiles_array.count(2048) / numiterations) * 100)
	plt.pie(result, labels=mylabels)
	plt.title("Percentage of Occurances:")

	plt.show()

