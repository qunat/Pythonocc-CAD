from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet

__author__ = 'magnus'


class TittleBarButton(QToolButton,QPushButton):
	def __init__(self,parent=None):
		QPushButton.__init__(self)
		sc = gui_scale()
		self.setMaximumWidth(30 * sc)
		self.setMinimumWidth(30 * sc)
		self.setMinimumHeight(50 * sc)
		self.setMaximumHeight(50 * sc)
		self.setStyleSheet(get_stylesheet("tittlebarButton"))
		self.setToolButtonStyle(3)
		self.setIconSize(QSize(32 * sc, 32 * sc))
		
		
class TittleBarButton_windown(QToolButton,QPushButton):
	def __init__(self,parent=None):
		QPushButton.__init__(self)
		sc = gui_scale()
		self.setMaximumWidth(50 * sc)
		self.setMinimumWidth(50 * sc)
		self.setMinimumHeight(50 * sc)
		self.setMaximumHeight(50 * sc)
		self.setStyleSheet(get_stylesheet("tittlebarButtonWindown"))
		self.setToolButtonStyle(3)
		self.setIconSize(QSize(32 * sc, 32 * sc))

		
	 
	
	
		
