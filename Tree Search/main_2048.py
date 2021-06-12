import numpy as np
import random
from itertools import product, combinations
import math
import random
from datetime import datetime
import matplotlib.pyplot as plt
import game_gui as gg
import time
import pandas as pd
import sys

def initialize_game(size):
	board = np.zeros((size*size))
	initial_twos =  np.random.default_rng().choice(16, 2, replace=False)
	board[initial_twos] = 2
	board = board.reshape((size, size))

	return board

class Board:
	def __init__(self, size, simulation):
		random.seed(datetime.now())
		self.board = initialize_game(size)
		self.size = size
		self.WIN_VALUE = 2048
		self.TILES_RANDOM = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
		self.SEARCH_LENGTH = 10
		self.NUMBER_OF_SEARCHES = 50
		self.DIRECTIONS = ["DOWN", "UP", "LEFT", "RIGHT"]
		self.INVALID_MOVES = 10
		self.SIMULATION = simulation

        
	def change_board(self, array):
		self.board = array

	def slide_right(self, a_row):
		a_row = np.concatenate((a_row[a_row==0], a_row[a_row!=0]))
		return a_row
	
	def slide_right_1(self):
		self.board = np.apply_along_axis(self.slide_right, 1, self.board)
	
	def slide_right_2(self):
		new = np.zeros((self.size, self.size))
		done = False
		for i in range(4):
			count = self.size-1
			for j in range(self.size-1, -1, -1):
				if self.board[i][j] != 0:
					new[i][count] = self.board[i][j]
					if j != count:
						done = True
					count -= 1
		self.change_board(new)
		return done

	def merge_elements(self):
		for col in range(self.size-1, 0, -1):
			same_to_left_mask = np.equal(self.board[:, col], self.board[:, col-1])
			self.board[:, col] = np.multiply(1+same_to_left_mask, self.board[:,col])
			self.board[:, col-1] = np.multiply(np.logical_not(same_to_left_mask), self.board[:,col-1])
	
	def merge_elements_2(self):
		done = False
		for i in range(4):
			for j in range(3, 0, -1):
				if self.board[i][j] == self.board[i][j-1] and self.board[i][j] != 0:
					self.board[i][j] *= 2
					self.board[i][j-1] = 0
					done = True
		return done

	def perform_move(self, direction):
		if direction == "DOWN":
			self.board = np.rot90(self.board)
			has_pushed = self.slide_right_2()
			has_merged = self.merge_elements_2()
			self.slide_right_2()
			self.board = np.rot90(self.board, 3)
			move_made =  has_pushed or has_merged
		elif direction == "UP":
			self.board = np.rot90(self.board, 3)
			has_pushed = self.slide_right_2()
			has_merged = self.merge_elements_2()
			self.slide_right_2()
			self.board = np.rot90(self.board)
			move_made =  has_pushed or has_merged

		elif direction == "LEFT":
			self.board = np.rot90(self.board, 2)
			has_pushed = self.slide_right_2()
			has_merged = self.merge_elements_2()
			self.slide_right_2()
			self.board = np.rot90(self.board, 2)
			move_made =  has_pushed or has_merged

		elif direction == "RIGHT":
			has_pushed = self.slide_right_2()
			has_merged = self.merge_elements_2()
			self.slide_right_2()
			move_made =  has_pushed or has_merged
		else:
			pass

		if move_made:
			tile_value = self.TILES_RANDOM[random.randint(0, len(self.TILES_RANDOM)-1)]
			tile_row_options, tile_col_options = np.nonzero(np.logical_not(self.board))
			tile_location = random.randint(0, len(tile_row_options)-1)
			self.board[tile_row_options[tile_location], tile_col_options[tile_location]] = tile_value

		return move_made

	def check_for_win(self):
		is_win = False
		for row in range(self.size):
			for col in range(self.size):
				if self.board[row][col] == self.WIN_VALUE:
					is_win = True
		return is_win

	def check_for_loss(self):
		is_loss = True
		actual_board = np.copy(self.board)
		for move in self.DIRECTIONS:
			if self.perform_move(move):
				is_loss = False
				self.change_board(actual_board)
				break
			else:
				self.change_board(actual_board)
		return is_loss
			
	def board_evaluation(self):
		if self.check_for_win():
			return 2
		elif self.check_for_loss():
			return 0
		else:
			score = 0
			score += (16 - np.count_nonzero(self.board)) / 16
			if np.argmax(self.board) in [0, 3, 12, 15]:
				score *= 1.5


			return score
	
	def mover(self):
		
		actual_board = np.copy(self.board)
		move_results = np.zeros(4)
		move_results = np.zeros(4)
		#game_gui = gg.Game_gui()

		for first_move in range(4):
			for _ in range(self.NUMBER_OF_SEARCHES):
				move_was_made = self.perform_move(self.DIRECTIONS[first_move])
				 
				if not move_was_made:
					break
				INVALID_MOVES = 0
				step = 0
				while step < self.SEARCH_LENGTH:
					direction = self.DIRECTIONS[random.randint(0, 3)]
					move_was_made = self.perform_move(direction)
					if move_was_made:
						step += 1
					else: 
						INVALID_MOVES += 1
					if INVALID_MOVES == self.INVALID_MOVES:
						break
				evaluation = self.board_evaluation()
				move_results[first_move] += evaluation
				self.change_board(actual_board)
			if self.SIMULATION :

				game_gui.update_GUI(self.board.astype(int),self.board_evaluation())


		move = move_results.argmax()
		# print(self.DIRECTIONS[move])


		return self.perform_move(self.DIRECTIONS[move])
	
	def test_ai(self):
		slide_number = 0

		while slide_number < 1100:
			slide_number += 1
			# print(self.board)
			print(slide_number)
			is_not_stuck = self.mover()

			if slide_number > 930:
				if self.check_for_win():
					print('AI Won ')
					return "Win"
			if not is_not_stuck:
				print("AI Lost")
				print(self.board)
				return "Loss"
		return slide_number, 

eval_df = pd.DataFrame(columns=[128, 256, 512, 1024, 2048])

f = open("results_2.txt", "w")
for i in range(20):
	board = Board(4, simulation=sys.argv[0])
	if board.SIMULATION:
		game_gui = gg.Game_gui()

	result = board.test_ai()
	if result == "Win":
		f.write("1")
	elif result == "Loss":
		f.write("0")
	else: 
		f.write("Incomplete")
	flat_board = list(board.board.astype(int).flatten())
	for col in eval_df.columns:
		if col in flat_board:
			eval_df.loc()[len(eval_df),[col]] = 1

	if board.SIMULATION:
		game_gui.update_GUI(board.board.astype(int),result)
		game_gui.mainloop()

f.close()
