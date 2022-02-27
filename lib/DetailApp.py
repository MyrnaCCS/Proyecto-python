from tkinter import *
from PIL import ImageTk, Image
import PIL.Image
import pandas as pd
import os
import sys
sys.path.append('../')

class DetailApp(Tk):
	def __init__(self, character_name):
		Tk.__init__(self)
		# Initial Tk configuration
		Tk.geometry(self, '420x180') # Window size
		# Frame Configuration
		detail_frame = Frame(self)
		detail_frame.pack(side='top', fill='both')
		# Show window
		self.detail_frame = DetailScreen(detail_frame, self, character_name)
		self.detail_frame.grid(row=0, column=0, sticky="nsew")
		self.detail_frame.tkraise()


class DetailScreen(Frame):
	def __init__(self, parent, root, character_name):
		Frame.__init__(self, parent)
		# # Open detail csv
		self.info = pd.read_csv(os.path.join('info', character_name.lower()+'_info.csv'))
		self.skills = pd.read_csv(os.path.join('skills', character_name.lower()+'_skills.csv'), index_col='Skill')
		# Name and type
		label_character_name = Label(self, text=character_name+': '+self.info['Type'][0])
		label_character_name.pack(side=TOP)
		# Advantage
		msg = 'Advantage with: '
		for elem in self.info['Advantage with'].values:
			msg += elem + ', '
		label_character_advantage = Label(self, text=msg[:-2])
		label_character_advantage.pack(side=TOP)
		# No-advantage
		msg = 'Disadvantage with: '
		for elem in self.info['No-advantage with'].values:
			msg += elem + ', '
		label_character_no_advantage = Label(self, text=msg[:-2])
		label_character_no_advantage.pack(side=TOP)
		# Normal
		msg = 'Normal with: '
		for elem in self.info['Normal with'].values:
			msg += elem + ', '
		label_character_normal = Label(self, text=msg[:-2])
		label_character_normal.pack(side=TOP)
		# Skills
		msg = 'Skill | norm|At vent|At disadv|pot norm|pot adv|pot disadv|'
		label_skill = Label(self, text=msg)
		label_skill.pack(padx=0, pady=10)
		# Skills
		skill = self.skills.index.values[0]
		msg = skill + ' |'
		for pt in self.skills.loc[skill]:
			msg += str(pt) + 'pt|'
		label_skill = Label(self, text=msg)
		label_skill.pack(padx=0, )
		# Skills
		skill = self.skills.index.values[1]
		msg = skill + ' |' + str(self.skills.loc[skill][0]) + 'pt|'
		label_skill = Label(self, text=msg)
		label_skill.pack(padx=0)
		# Skills
		skill = self.skills.index.values[2]
		msg = skill + ' |' + str(self.skills.loc[skill][0]) + 'pt|'
		label_skill = Label(self, text=msg)
		label_skill.pack(padx=0)
		# Skills
		skill = self.skills.index.values[3]
		msg = skill + ' |' + 'Potenciador de campo, 1 vez cada 3 turnos. \n | tiene una duracion de 2 turnos.'
		label_skill = Label(self, text=msg)
		label_skill.pack(padx=0)