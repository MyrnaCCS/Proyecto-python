import random
import time
import pandas as pd
import sys
sys.path.append('../')

from lib.Battle import *

class Game(object):
	"""docstring for Game"""
	def __init__(self, character_name):
		super(Game, self).__init__()
		self.character_name = character_name
		self.battle = None


class TrainingGame(Game):
	def __init__(self, character_name, opponent_name):
		super(TrainingGame, self).__init__(character_name)
		self.opponent_name = opponent_name
		self.battle = None

	def start_battle(self):
		self.battle = Battle(self.character_name, self.opponent_name)
		is_player_first = self.battle.start()
		return is_player_first

	def get_battle(self):
		return self.battle

class StoryGame(Game):
	def __init__(self, character_name, user_name):
		super(StoryGame, self).__init__(character_name)
		self.opponents_list = sorted(['Aquarder', 'Electder', 'Firesor', 'Mousebug', 'Rockdog', 'Splant']) # Change for csv
		self.user_info = pd.read_csv(os.path.join('users', user_name + '.csv'))

	def start_battle(self):
		opponent_name = self.opponents_list[self.user_info['Level'][0]]
		self.battle = Battle(self.character_name, opponent_name.lower())
		is_player_first = self.battle.start()
		return is_player_first

	def get_battle(self):
		return self.battle

	def get_opponent_name(self):
		return self.opponents_list[self.user_info['Level'][0]]

	def increase_level(self):
		if self.opponents_list[self.user_info['Level'][0]] == self.opponents_list[-1]:
			os.remove(os.path.join('users', self.user_info['User'][0] + '.csv'))
		else:
			# save
			self.user_info['Level'] += 1
			self.user_info.to_csv(os.path.join('users', self.user_info['User'][0] + '.csv'), index=False)

	def restart_game(self):
		self.user_info['Level'] = 0
		self.user_info.to_csv(os.path.join('users', self.user_info['User'][0] + '.csv'), index=False)