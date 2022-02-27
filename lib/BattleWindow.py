from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import PIL.Image
from glob import glob
import os
import time
import sys
sys.path.append('../')

LARGE_FONT = ('HelvLight', 10)

class BattleApp(Tk):
	def __init__(self, args):
		Tk.__init__(self)
		# Initial Tk configuration
		Tk.title(self, '')
		Tk.geometry(self, '500x250') # Window size
		# Initial Frame Configuration
		init_frame = Frame(self)
		init_frame.pack(side='top', fill='both', expand=True)
		# Configure grid (3 x 4)
		for i in range(3):
			init_frame.grid_columnconfigure(i, weight=1)
			init_frame.grid_rowconfigure(i, weight=1)
		init_frame.grid_rowconfigure(3, weight=1)
		init_frame.grid_rowconfigure(4, weight=1)
		# Aquí start battle
		self.battle = args['Battle']
		self.character_name = args['Character name']
		self.opponent_name = args['Opponent name']
		is_player_first = self.battle.start()
		if is_player_first:
			state = NORMAL
		else:
			state = DISABLED
		# Show battle window
		fargs = {'State': state,
				 'Character name': self.character_name,
				 'Opponent name': self.opponent_name,
				 'Character skill names': self.battle.get_character_skills_list()}
		self.frame = BattleScreen(init_frame, self, fargs)
		self.frame.grid(row=0, column=0, sticky="nsew")	
		self.frame.tkraise()
		if not is_player_first:
			self.frame.update()
			self.after(1000, self.set_cpu_attack())


	def set_player_attack(self, attack_name):
		hp_opponent, is_you_win = self.battle.player_turn(attack_name)
		if is_you_win:
			self.win()
		else:
			self.frame.actualize_message_label(self.character_name + ' used ' + attack_name)
			self.frame.actualize_cpu_hp(hp_opponent)
			self.frame.deactivate_attacks()
			self.frame.update()
			self.after(1000, self.set_cpu_attack())
			

	def set_cpu_attack(self):
		hp_character, is_game_over, attack_name = self.battle.cpu_turn()
		if is_game_over:
			self.game_over()
		else:
			self.frame.actualize_message_label(self.opponent_name + ' used ' + attack_name)
			self.frame.actualize_player_hp(hp_character)
			self.after(1000, self.frame.activate_attacks())
			is_enhancer_available = self.battle.is_enhancer_available()
			if not is_enhancer_available:
				self.frame.deactivate_enhancer_button()
	
	def win(self):
		self.frame.actualize_message_label('You win!')
		self.after(1000, self.destroy())

	def game_over(self):
		self.frame.actualize_message_label('Game over!')
		self.after(1000, self.destroy())



class BattleScreen(Frame):
	def __init__(self, parent, root, fargs):
		Frame.__init__(self, parent)
		# Get the skill names
		self.skill_names_list = fargs['Character skill names']
		# Option: int var to get the clicked button
		self.option = IntVar()
		# Button skills list
		self.button_skill_names_list = []
		for idx, skill in enumerate(self.skill_names_list):
			self.button_skill_names_list.append(Radiobutton(self, text=skill, variable=self.option, value=idx, indicator=0, command=lambda: root.set_player_attack(self.skill_names_list[self.option.get()]), state=fargs['State']))
			self.button_skill_names_list[idx].grid(row=idx+1, column=0)
		# Label character image, name, hp
		character_name = fargs['Character name']
		icon_character = self.get_icon(character_name.lower())
		label_character_icon = Label(self, image=icon_character)
		label_character_icon.image = icon_character
		label_character_icon.grid(row=0, column=1)
		label_character_name = Label(self, text=character_name)
		label_character_name.grid(row=2, column=1)
		self.player_hp = StringVar(value='25 Hp')
		label_character_hp = Label(self, textvariable=self.player_hp)
		label_character_hp.grid(row=3, column=1)
		# Label opponent image, name, hp
		opponent_name = fargs['Opponent name']
		icon_opponent = self.get_icon(opponent_name.lower())
		label_opponent_icon = Label(self, image=icon_opponent)
		label_opponent_icon.image = icon_opponent
		label_opponent_icon.grid(row=0, column=2)
		label_opponent_name = Label(self, text=opponent_name)
		label_opponent_name.grid(row=2, column=2)
		self.cpu_hp = StringVar(value='25 Hp')
		label_opponent_hp = Label(self, textvariable=self.cpu_hp)
		label_opponent_hp.grid(row=3, column=2)
		# Label messages
		self.message = StringVar(value='Hello!')
		label_messages = Label(self, textvariable=self.message, font=LARGE_FONT)
		label_messages.grid(row=5, column=1)

	def get_icon(self, nekomon_name):
		path = os.path.join('images', nekomon_name + '.png')
		icon = Image.open(path)
		icon = icon.resize((150,150))
		icon = ImageTk.PhotoImage(icon)
		return icon

	def actualize_player_hp(self, hp):
		msg = str(hp) + 'Hp'
		self.player_hp.set(msg)

	def actualize_cpu_hp(self, hp):
		msg = str(hp) + 'Hp'
		self.cpu_hp.set(msg)

	def activate_attacks(self):
		for button in self.button_skill_names_list:
			button.config(state = NORMAL)

	def deactivate_attacks(self):
		for button in self.button_skill_names_list:
			button.config(state = DISABLED)

	def actualize_message_label(self, msg):
		self.message.set(msg)

	def activate_button(self, idx=-1):
		self.button_skill_names_list[idx].config(state=NORMAL)

	def deactivate_enhancer_button(self, idx=-1):
		self.button_skill_names_list[idx].config(state=DISABLED)