# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt5 import QtWidgets,QtGui,QtCore
from module import DisplayManager

class modulewindowmanager(object):
	def __init__(self,parent=None):
		self.parent=parent
	def CreatePartWindown(self):
		pass
		app = QtWidgets.QApplication.instance()
		if not app:
			app = QtWidgets.QApplication(sys.argv)

		self.parent.change_ribbon("RibbonMain")#change part ribbon 
		# Create a tab widget
		self.tabwidget = QTabWidget(self.parent)

        # Create tabs
		tab1 = QWidget()
		tab2 = QWidget()

		# Add tabs to the tab widget
		self.parent.Displayshape_core=DisplayManager.DisplayManager(self.parent)
		self.tabwidget.addTab(self.parent.Displayshape_core.canva, "零件1")
		#self.tabwidget.addTab(tab2, "Tab 2")
		self.parent.setCentralWidget(self.tabwidget)
		self.parent.Displayshape_core.canva.InitDriver()
		self.parent.Displayshape_core.canva.qApp = app
		self.parent.Displayshape_core.canva._display.display_triedron()
		self.parent.Displayshape_core.Displaydatum()
		self.parent.Displayshape_core.SetBackgroundImage()
		self.parent.Displayshape_core.DisplayCube()
		self.parent.Displayshape_core.canva._display.Repaint()
		self.tabwidget.repaint()
		self.tabwidget.setFocus()
		self.tabwidget.setCurrentIndex(0)
		QApplication.processEvents()
		
		


	def CreateAssembelyWindown(self):
		pass
	def CreateSheetWindown(self):
		pass