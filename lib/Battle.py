import random
from lib.Characters import *

class Battle(object):
	def __init__(self, character_name, opponent_name):
		self.character = Character(character_name.lower())
		self.opponent = Character(opponent_name)
		self.is_character_first = bool(random.randint(0, 1))
		self.character.set_attack_mode(self.opponent.get_type())
		self.opponent.set_attack_mode(self.character.get_type())
		self.is_game_over = None

	def start(self):
		return self.is_character_first

	def get_character_skills_list(self):
		return self.character.get_skills()

	def is_enhancer_available(self):
		return self.character.is_enhancer_available()

	def is_win(self):
		return not self.is_game_over

	def player_turn(self, attack_name):
		points = self.character.get_attack_points(attack_name)
		hp_opponent = self.opponent.recive_attack(points)
		if hp_opponent <= 0:
			is_you_win = True
		else:
			is_you_win = False
			self.is_game_over = False
		return hp_opponent, is_you_win

	def cpu_turn(self):
		points = -1
		while points < 0:
			idx_attack = random.randint(0, len(self.opponent.get_skills())-1)
			attack_name = self.opponent.get_skills()[idx_attack]
			points = self.opponent.get_attack_points(attack_name)
		hp_character = self.character.recive_attack(points)
		if hp_character <= 0:
			is_game_over = True
			self.is_game_over = True
		else:
			is_game_over = False
		return hp_character, is_game_over, attack_name