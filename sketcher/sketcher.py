# -*- coding: utf-8 -*-
from GUI.SelectWidget import SelectWidget

class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
	
		
	def select_skecth_plane(self):
		self.select_windows=SelectWidget(parent=self.parent)
		self.select_windows.Show()
		
	def fun(self):
		self.parent.InteractiveOperate.InteractiveModule="SKETCH"
		if self.select_windows.comboBox.currentText()=="XY平面":
			self.parent.Displayshape_core.canva.View_Left()
			self.parent.Displayshape_core.canva._display.FitAll()
	