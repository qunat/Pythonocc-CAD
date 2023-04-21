# -*- coding: utf-8 -*-
from GUI.SelectWidget import SelectWidget

class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
	
		
	def select_skecth_plane(self):
		self.select_windows=SelectWidget(parent=self.parent)
		self.select_windows.Show()
		
	def uptoplane(self):
		self.parent.InteractiveOperate.InteractiveModule="SKETCH"
		if self.select_windows.comboBox.currentText()=="XY平面":
			self.parent.Displayshape_core.canva._display.View_Front()
			self.parent.Displayshape_core.canva._display.FitAll()
		if self.select_windows.comboBox.currentText()=="YZ平面":
			self.parent.Displayshape_core.canva._display.View_Bottom()
			self.parent.Displayshape_core.canva._display.FitAll()
		if self.select_windows.comboBox.currentText()=="XZ平面":
			self.parent.Displayshape_core.canva._display.View_Right()
			self.parent.Displayshape_core.canva._display.FitAll()

	