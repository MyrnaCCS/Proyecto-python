import tkinter as tk
from tkinter import messagebox
import os

from lib.TrainingMode import *
from lib.StoryMode import *

LARGE_FONT= ('HelvLight', 20)

class ModeWindows(tk.Tk):
	def __init__(self, user_name):
		# Initial Tk configuration
		tk.Tk.__init__(self)
		tk.Tk.title(self, '')
		tk.Tk.geometry(self, '150x160') # window size
		# Initial Frame Configuration
		container = tk.Frame(self)
		container.pack(side='top', fill='both')
		# Show window
		self.frame = ModeWindow(container, self)
		self.frame.grid(row=0, column=0, sticky="nsew")
		self.frame.tkraise()
		self.user_name = user_name

	def story_windows(self):
		self.destroy()
		app = StoryApp(self.user_name)
		app.mainloop()
		self.__init__(self.user_name)

	def training_windows(self):
		self.destroy()
		app = TrainingApp()
		app.mainloop()
		self.__init__(self.user_name)


class ModeWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		window_objects_list = []
		# Title
		window_objects_list.append(tk.Label(self, text="NEKOMON", font=LARGE_FONT))
		# Story Mode Button
		window_objects_list.append(tk.Button(self, text='Story Mode', command=lambda:controller.story_windows()))
		# Training Mode Button
		window_objects_list.append(tk.Button(self, text='Training Mode', command=lambda:controller.training_windows()))
		# Pack
		for obj in window_objects_list:
			obj.pack(padx=15, pady=10, side=TOP)