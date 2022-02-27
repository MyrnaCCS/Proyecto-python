from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import PIL.Image
from glob import glob
import os
import sys
sys.path.append('../')

from lib.Game import StoryGame
from lib.DetailApp import *
from lib.BattleWindow import *
from lib.ModeWindows import *
from lib.TrainingMode import CharacterScreen

LARGE_FONT = ('HelvLight', 10)

class StoryApp(Tk):
	def __init__(self, user_name):
		Tk.__init__(self)
		# Initial Tk configuration
		Tk.title(self, '')
		Tk.geometry(self, '300x300') # Window size
		# Initial Frame Configuration
		init_frame = Frame(self)
		init_frame.pack(side='top', fill='both', expand=True)
		# Configure grid (3 x 4)
		for i in range(3):
			init_frame.grid_columnconfigure(i, weight=1)
			init_frame.grid_rowconfigure(i, weight=1)
		init_frame.grid_rowconfigure(3, weight=1)
		init_frame.grid_rowconfigure(4, weight=1)
		# Init Training Game
		self.is_character_choosed = False
		self.character_name = None
		# Show window
		self.frame = CharacterScreen(init_frame, self)
		self.frame.grid(row=0, column=0, sticky="nsew")
		self.frame.tkraise()
		self.user_name = user_name

	def show_detail(self, character_name):
		detail_app = DetailApp(character_name)
		detail_app.mainloop()

	def nekomon_choosed(self, character_name):
		self.character_name = character_name
		self.frame.change_character_color(character_name)
		if not self.is_character_choosed:
			self.frame.activate_start_button()
		else:
			self.is_character_choosed = True
		
	def start_game(self):
		self.destroy()
		# Init story
		self.game = StoryGame(self.character_name, self.user_name)
		# Init battle
		self.game.start_battle()
		self.battle = self.game.get_battle()
		# Args
		args = {'Character name': self.character_name,
				'Opponent name': self.game.get_opponent_name(),
				'Battle': self.battle}
		app = BattleApp(args)
		app.mainloop()
		is_you_win = self.battle.is_win()
		if is_you_win:
			self.game.increase_level()
			self.__init__(self.user_name) # Next battle
		else:
			Tk.__init__(self)
			try_again = messagebox.askokcancel(title='Game over', message='Do you want to try again?')
			self.destroy()
			if try_again:
				self.__init__(self.user_name)
			else:
				self.game.restart_game()