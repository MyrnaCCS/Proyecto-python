from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import PIL.Image
from glob import glob
import os
import sys
sys.path.append('../')

from lib.Game import TrainingGame
from lib.DetailApp import *
from lib.BattleWindow import *

LARGE_FONT = ('HelvLight', 10)

class TrainingApp(Tk):
	def __init__(self):
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
			init_frame.grid_rowconfigure(2*i, weight=1)
			init_frame.grid_rowconfigure(2*i+1, weight=1)
		# Init Training Game
		'''self.game = TrainingGame()'''
		self.is_character_choosed = False
		self.character_name = None
		self.opponent_name = None
		# Show window
		self.frame = CharacterScreen(init_frame, self)
		self.frame.grid(row=0, column=0, sticky="nsew")
		self.frame.tkraise()

	def show_detail(self, character_name):
		detail_app = DetailApp(character_name)
		detail_app.mainloop()

	def nekomon_choosed(self, character_name):
		# change to some color
		if self.is_character_choosed:
			self.frame.change_opponent_color(character_name)
			if self.opponent_name is None:
				self.frame.activate_start_button()
			self.opponent_name = character_name
		else:
			self.frame.change_character_color(character_name)
			go_on = messagebox.askokcancel(title='Go on', message='Do you want to choose your opponent?')
			if go_on:
				self.character_name = character_name
				self.is_character_choosed = True
	
	def start_game(self):
		self.destroy()
		# Init training
		self.game = TrainingGame(self.character_name, self.opponent_name)
		self.game.start_battle()
		self.battle = self.game.get_battle()
		# Agrs to init battle
		args = {'Character name': self.character_name,
				'Opponent name': self.opponent_name,
				'Battle': self.battle}
		app = BattleApp(args)
		app.mainloop()
		self.__init__()

class CharacterScreen(Frame):
	def __init__(self, parent, root):
		Frame.__init__(self, parent)
		# Icons directory
		icons_dir_paths = sorted(glob(os.path.join('images', '*' + '.png')))
		# Characters list
		character_names = sorted(['Aquarder', 'Electder', 'Firesor', 'Mousebug', 'Rockdog', 'Splant'])
		# Var: option, option_detail
		self.option = IntVar(value=10)
		self.option_detail = IntVar(value=10)
		self.button_character_dict = {}
		for character, path in zip(enumerate(character_names), icons_dir_paths):
			# Get icon as ImageTk
			icon = PIL.Image.open(path)
			icon = icon.resize((100,100))
			icon = ImageTk.PhotoImage(icon)
			# Label character name
			idx_row = 3 * (character[0] // 3)
			idx_col = character[0] % 3
			label_character_name = Label(self, text=character[1], font=LARGE_FONT)
			label_character_name.grid(row=idx_row, column=idx_col)
			# Button to choose character
			self.button_character_dict[character[1]] = Radiobutton(self, image=icon, variable=self.option, value=character[0], indicator=0, command=lambda:root.nekomon_choosed(character_names[self.option.get()]), bg='white')
			self.button_character_dict[character[1]].image = icon
			self.button_character_dict[character[1]].grid(row=idx_row+1, column=idx_col)
			# Button character detail
			button_character_detail = Radiobutton(self, text='Detail', variable=self.option_detail, value=character[0], indicator=0, command=lambda:root.show_detail(character_names[self.option_detail.get()]))
			button_character_detail.grid(row=idx_row+2, column=idx_col)
		# Choose button
		self.button_start = Button(self, text='Start', command=lambda:root.start_game(), state=DISABLED)
		self.button_start.grid(row=6, column=1)

	def change_character_color(self, character_name):
		for button in self.button_character_dict.values():
			if button.cget('bg') == 'blue':
				button.config(bg='white')
		self.button_character_dict[character_name].config(bg='blue')
		self.option.set(10)

	def change_opponent_color(self, character_name):
		for button in self.button_character_dict.values():
			if button.cget('bg') == 'red':
				button.config(bg='white')
		self.button_character_dict[character_name].config(bg='red')
		self.option.set(10)

	def activate_start_button(self):
		self.button_start.config(state=NORMAL)