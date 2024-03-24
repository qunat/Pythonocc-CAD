# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,QDockWidget
from PyQt5 import QtWidgets,QtGui,QtCore
from module import DisplayManager
from GUI.TopBorderBarWidge import *
class modulewindowmanager(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.modulewindowname_dict={}
		self.parent.Displayshape_core_dict={}
		self.windownname=["零件1"]


	def CreatePartWindown(self):
		app = QtWidgets.QApplication.instance()
		if not app:
			app = QtWidgets.QApplication(sys.argv)

		self.parent.change_ribbon("RibbonMain")  #change part ribbon 
		# Create a tab widget
		self.tabwidget = QTabWidget(self.parent)
		self.tabwidget.setTabsClosable(True)
		# Add tabs to the tab widget
		self.parent.Displayshape_core_dict[self.windownname[0]]=DisplayManager.DisplayManager(self.parent)
		self.tabwidget.addTab(self.parent.Displayshape_core_dict[self.windownname[0]].canva, "零件1")
		self.parent.setCentralWidget(self.tabwidget)
		self.parent.Displayshape_core_dict[self.windownname[0]].canva.InitDriver()
		self.parent.Displayshape_core_dict[self.windownname[0]].canva.qApp = app
		self.parent.Displayshape_core_dict[self.windownname[0]].canva._display.display_triedron()
		self.parent.Displayshape_core_dict[self.windownname[0]].Displaydatum()
		self.parent.Displayshape_core_dict[self.windownname[0]].SetBackgroundImage()
		self.parent.Displayshape_core_dict[self.windownname[0]].DisplayCube()
		self.parent.Displayshape_core_dict[self.windownname[0]].canva._display.Repaint()
		self.parent.Displayshape_core_dict[self.windownname[0]].canva.setFocus()
		self.tabwidget.repaint()
		self.tabwidget.setFocus()
		self.tabwidget.setCurrentIndex(1)
		self.tabwidget.setCurrentIndex(0)
		self.parent.repaint()


		#Create ModelTree
		self.items = QDockWidget('组合浏览器', self.parent)  # 新建QDockWidget
		self.parent.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.items)  # 在主显示区域右侧显示
		self.items.setMinimumWidth(280)# 设置最小大小
		self.items.setWidget(self.parent.modeltree.tree)
		
		#Create TopBorderBar
		self.TopBorderBa=TopBorderBarWidget(self.parent)
		self.parent.addToolBar(QtCore.Qt.TopToolBarArea, self.TopBorderBa)
		self.parent.insertToolBarBreak(self.TopBorderBa)


	def CreateAssembelyWindown(self):
		pass
	def CreateSheetWindown(self):
		pass