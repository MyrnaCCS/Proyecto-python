import pandas as pd
import os

class Character(object):
	"""docstring for Character"""
	def __init__(self, character_name):
		self.name = character_name.lower()
		self.type = None
		self.skills = self.read_skills()
		self.info = self.read_info()
		self.hp = 25
		self.attack_mode = None
		self.enhancer = False
		self.rest_turns_with_enhancer = 2
		self.counter_turns_after_enhanced = 1e3

	def read_skills(self):
		skills = pd.read_csv(os.path.join('skills', self.name+'_skills.csv'), index_col='Skill')
		return skills

	def read_info(self):
		info = pd.read_csv(os.path.join('info', self.name+'_info.csv'))
		self.my_type = info['Type'][0]
		return info

	def set_attack_mode(self, opponent_type):
		if opponent_type in self.info['Advantage with'].values:
			self.attack_mode = 'Advantage'
		elif opponent_type in self.info['No-advantage with'].values:
			self.attack_mode = 'No-advantage'
		else:
			self.attack_mode = 'Normal'

	def get_skills(self):
		return self.skills.index.values

	def get_type(self):
		return self.my_type

	def is_enhancer_available(self):
		if self.rest_turns_with_enhancer > 0 and self.counter_turns_after_enhanced >= 3 and not self.enhancer:
			return True
		else:
			return False

	def set_enhanced_mode(self):
		if self.rest_turns_with_enhancer > 0 and self.counter_turns_after_enhanced >= 3:
			self.enhancer = True
			# Recet counter of turns with no enhancer mode
			self.counter_turns_after_enhanced = 0 
			points = 0
		else:
			points = -1 # Error
		return points

	def get_attack_points(self, attack_name):
		list_attack_points = self.skills.loc[attack_name]
		# Is enhancer activation?
		is_enhanced = pd.isna(list_attack_points['Normal attack'])
		if is_enhanced:
			return self.set_enhanced_mode()
		else:
			self.counter_turns_after_enhanced += 1
		# If is not enhacer activation
		is_normal = pd.isna(list_attack_points['Advantage attack'])
		if is_normal:
			points = list_attack_points['Normal attack']
		else:
			if self.enhancer:
				attack_mode_str = self.attack_mode + ' enhanced attack'
				# Using enhanced mode
				self.rest_turns_with_enhancer -= 1
				self.enhancer = False
			else:
				attack_mode_str = self.attack_mode + ' attack'
			points = list_attack_points[attack_mode_str]
		return points

	def recive_attack(self, points):
		self.hp -= points
		return self.hp