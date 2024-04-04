# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,QDockWidget
from PyQt5 import QtWidgets,QtGui,QtCore
from module import DisplayManager,ModelTree
from GUI.TopBorderBarWidge import *
from GUI.ViewLeaderWidget import *

class modulewindowmanager(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.items=None
		self.TopBorderBa=None
		# Create a tab widget
		self.tabwidget = QTabWidget(self.parent)
		self.tabwidget.setTabsClosable(True)
		# initial windownname number
		self.modulewindowname_dict={}
		self.parent.Displayshape_core_dict={}
		self.parent.modeltree_dict={}
		self.ViewleaderBar_dict={}
		self.windownname=["零件1"]
		self.windownnum=1
		self.tabwidget.currentChanged.connect(self.TabwidgetChangeEvent)


	def CreatePartWindown(self,name=None):
		app = QtWidgets.QApplication.instance()
		if not app:
			app = QtWidgets.QApplication(sys.argv)
		
		if name==None:
			self.CreateWindownname()
		else:
			self.windownname.append(name)

		self.parent.current_window_name=self.windownname[-1]
		# Add tabs to the tab widget
		self.parent.Displayshape_core_dict[self.windownname[-1]]=DisplayManager.DisplayManager(self.parent)
		self.tabwidget.addTab(self.parent.Displayshape_core_dict[self.windownname[-1]].canva, self.windownname[-1])
		self.parent.setCentralWidget(self.tabwidget)
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.InitDriver()
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.qApp = app
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.display_triedron()
		self.parent.Displayshape_core_dict[self.windownname[-1]].Displaydatum()
		self.parent.Displayshape_core_dict[self.windownname[-1]].SetBackgroundImage()
		self.parent.Displayshape_core_dict[self.windownname[-1]].DisplayCube()
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.Repaint()
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.setFocus()
		self.tabwidget.setCurrentIndex(self.tabwidget.count()-1)
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.OnResize()
		self.tabwidget.update()
		self.tabwidget.repaint()
		self.tabwidget.setFocus()
		self.parent.repaint()
		#self.ViewleaderBar_dict[self.windownname[-1]]=ViewLeaderWidget(self.parent.Displayshape_core_dict[self.windownname[-1]].canva)
		
		#change part ribbon 
		if self.items==None and self.TopBorderBa==None:
			self.parent.change_ribbon("RibbonMain")  

		#Create ModelTree
		if self.items==None:
			self.items = QDockWidget('组合浏览器', self.parent)  # 新建QDockWidget
			self.parent.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.items)  # 在主显示区域右侧显示
			self.items.setMinimumWidth(280)# 设置最小大小
		self.parent.modeltree_dict[self.windownname[-1]]=ModelTree.ModelTree()
		self.items.setWidget(self.parent.modeltree_dict[self.windownname[-1]].tree)

		#Create TopBorderBar
		if self.TopBorderBa==None:	
			self.TopBorderBa=TopBorderBarWidget(self.parent)
			self.parent.addToolBar(QtCore.Qt.TopToolBarArea, self.TopBorderBa)
			self.parent.insertToolBarBreak(self.TopBorderBa)
		# reset TopBorderBa view
		self.TopBorderBa.reset_triggered_connect()
		

	def CreateWindownname(self):
		number=len(self.windownname)
		if number!=0:
			windownname="零件"+str(number)
			self.windownname.append(windownname)

	def CreateAssembelyWindown(self):
		pass
	def CreateSheetWindown(self):
		pass
	def TabwidgetChangeEvent(self):
		try:
			index=self.tabwidget.currentIndex()
			name=self.tabwidget.tabText(index)
			self.items.setWidget(self.parent.modeltree_dict[name].tree)
			self.parent.current_window_name=name
			self.TopBorderBa.reset_triggered_connect()
		except:
			pass