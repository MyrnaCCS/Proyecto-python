import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv

from lib.ModeWindows import *

import os
import sys
sys.path.append('../')

LARGE_FONT = ('HelvLight', 20)

class InitialWindows(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		# Initial Tk configuration
		tk.Tk.title(self, '')
		tk.Tk.geometry(self, '150x160') # Window size
		# Initial Frame Configuration
		container = tk.Frame(self)
		container.pack(side='top', fill='both')
		# Diferent kind of frames dict
		self.frames = {}
		for frame_class in (StartWindow, LogInWindow, SingInWindow, ModeWindow):
			frame = frame_class(container, self)
			self.frames[frame_class] = frame
			frame.grid(row=0, column=0, sticky="nsew")
		# Show Initial Window
		self.show_frame(StartWindow)

	def show_frame(self, container):
		frame = self.frames[container]
		frame.tkraise()

	def close_windows(self, user_name):
		self.destroy()
		app = ModeWindows(user_name)
		app.mainloop()



class StartWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		# Title
		label_title = tk.Label(self, text="NEKOMON", font=LARGE_FONT)
		label_title.pack(pady=10, padx=10)
		# Log In button
		button_log_in = tk.Button(self, text='Log In', command=lambda: controller.show_frame(LogInWindow))
		button_log_in.pack(pady=10)
		# Sing In button
		button_sing_in = tk.Button(self, text='Sing In', command=lambda: controller.show_frame(SingInWindow))
		button_sing_in.pack(pady=10)


class LogInWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		# Title
		label_title = tk.Label(self, text="NEKOMON", font=LARGE_FONT)
		label_title.pack(pady=10,padx=10)

		# User
		label_user = tk.Label(self, text='User Name')
		label_user.pack()
		self.entry_user = tk.Entry(self)
		self.entry_user.pack()

		# Password
		label_password = tk.Label(self, text='Password')
		label_password.pack()
		self.entry_password = tk.Entry(self)
		self.entry_password.pack()

		# Start Button
		start_button = tk.Button(self, text='Log In', command=self.user_validation)
		start_button.pack(pady=10)

	def user_validation(self):
		user = self.entry_user.get()
		password = self.entry_password.get()
		try:
			user_data = pd.read_csv(os.path.join('users', user+'.csv'))
			if password == user_data['Password'][0]:
				self.controller.close_windows(user) # Valid user then open mode window
			else:
				messagebox.showwarning(title='Wrong password', message='The password you entered is incorrect.')
				self.entry_password.delete(0, 100)
		except FileNotFoundError:
			new_user = messagebox.askokcancel(title='Wrong username', message='Do you want to register a new user?')
			if new_user:
				self.controller.show_frame(SingInWindow)
			else:
				self.entry_user.delete(0, 100)
				self.entry_password.delete(0, 100)


class SingInWindow(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		# Title
		label_title = tk.Label(self, text='NEKOMON', font=LARGE_FONT)
		label_title.pack(pady=10,padx=10)

		# User
		label_user = tk.Label(self, text='User Name')
		label_user.pack()
		self.entry_user = tk.Entry(self)
		self.entry_user.pack()

		# Password
		label_password = tk.Label(self, text='Password')
		label_password.pack()
		self.entry_password = tk.Entry(self)
		self.entry_password.pack()

		# Start Button
		start_button = tk.Button(self, text='Sing In', command=self.user_registration)
		start_button.pack(pady=10)

	def user_registration(self):
		user = self.entry_user.get()
		password = self.entry_password.get()
		try:
			user_data = pd.read_csv(os.path.join('users', user+'.csv'))
			messagebox.showwarning(title='User name already used', message='Try a different user name.')
			self.entry_user.delete(0, 100)
		except FileNotFoundError:
			data = [['User', 'Password', 'Level'], [user, str(password), 0]]
			file = open(os.path.join('users', user+'.csv'), 'w')
			with file:
				writer = csv.writer(file)
				writer.writerows(data)
			self.controller.close_windows(user) # Valid user then open mode window