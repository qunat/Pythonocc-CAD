from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5 import  QtWidgets,QtCore,QtGui,Qt
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet

__author__ = 'magnus'


class SketcherButton(QToolButton,QPushButton,QAction):
	def __init__(self,parent=None,object_name=None,icon_name=None,icon_size=[],action_tip=None,action=None,):
		QPushButton.__init__(self)
		sc = gui_scale()
		self.setMaximumWidth(25 * sc)
		self.setMinimumWidth(25 * sc)
		self.setMinimumHeight(50 * sc)
		self.setMaximumHeight(50 * sc)
		self.setStyleSheet(get_stylesheet("SketcherButton"))
		self.setToolButtonStyle(3)
		self.setIconSize(QSize(32 * sc, 32 * sc))
		self.Create_IconButton(parent,object_name,icon_name,icon_size,action_tip,action)
		
	def Create_IconButton(self,parent=None,object_name=None,icon_name=None,icon_size=None,action_tip=None,action=None):
		self.setObjectName(object_name)
		self.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/{}.png".format(icon_name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(icon_size[0],icon_size[1]))
		self.setToolTip(action_tip)
		self.Add_Action(action_1=action)
	
	def Add_Action(self, action_1=None):
		if action_1!=None:
			self.clicked.connect(action_1)
		
		
		
class TittleBarButton_windown(QToolButton,QPushButton):
	def __init__(self,parent=None,object_name=None,icon_name=None,icon_size=[],action=None):
		QPushButton.__init__(self)
		self.checked=1
		sc = gui_scale()
		self.setMaximumWidth(30 * sc)
		self.setMinimumWidth(30 * sc)
		self.setMinimumHeight(50 * sc)
		self.setMaximumHeight(50 * sc)
		self.setStyleSheet(get_stylesheet("tittlebarButtonWindown"))
		self.setToolButtonStyle(3)
		self.setIconSize(QSize(32 * sc, 32 * sc))
		self.Create_IconButton(parent, object_name, icon_name, icon_size, action)
		
	def Create_IconButton(self,parent=None,object_name=None,icon_name=None,icon_size=None,action=None):
		self.setObjectName(object_name)
		self.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/{}.png".format(icon_name)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setIcon(icon)
		self.setIconSize(QtCore.QSize(icon_size[0],icon_size[1]))

	def Add_Action(self,action_1=None,action_2=None):
		if action_1!=None and action_2!=None:
			def fun():
				if self.checked==1:
					action_1()
				if self.checked==-1:
					action_2()
				self.checked *= -1
				
			self.clicked.connect(fun)
		
		else:
			self.clicked.connect(action_1)
		pass
	 
	
	
		
