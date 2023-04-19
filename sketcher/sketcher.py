# -*- coding: utf-8 -*-
from GUI.SelectWidget import SelectWidget

class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
		
	def select_skecth_plane(self):
		select_windows=SelectWidget(parent=self.parent)
		select_windows.Show()