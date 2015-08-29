import pygame
from pgu import gui 

class Gui(object):
	def __init__(self, width=500, height=250):
		self.width = width
		self.height = height
		app = gui.App()
		container = gui.container(self.width, self.height)

	def drawButton(self, text):
		button = gui.Button(text)
		# app.connect(gui.CLICK)
		button.connect(gui.CLICK, app.click, None)
		container.add(button, 60, 30)