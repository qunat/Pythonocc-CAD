from PyQt5.QtWidgets import *
from GUI.RibbonTab import RibbonTab
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet
from PyQt5 import  QtWidgets,QtCore,QtGui

__author__ = 'loujiand'


class TittleBarWidget(QToolBar):
	def __init__(self, parent):
		QToolBar.__init__(self, parent)
		self.setStyleSheet(get_stylesheet("ribbon"))
		self.setObjectName("TittleWidget")
		self.setWindowTitle("Tittle")
		self._ribbon_widget = QTabWidget(self)
		self._ribbon_widget.setMaximumHeight(40*gui_scale())
		self._ribbon_widget.setMinimumHeight(40*gui_scale())
		self.setMovable(False)
		self.addWidget(self._ribbon_widget)
		
		self.pushButton = QtWidgets.QPushButton(self)
		self.pushButton.setGeometry(QtCore.QRect(4, 0, 40, 40))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/logo-no-background.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton.setIcon(icon)
		self.pushButton.setIconSize(QtCore.QSize(40, 40))
		
		self.pushButton_2 = QtWidgets.QPushButton(self)
		self.pushButton_2.setGeometry(QtCore.QRect(40, 5, 40, 40))
		self.pushButton_2.setObjectName("pushButton")
		self.pushButton_2.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/undo_system_bar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_2.setIcon(icon)
		self.pushButton_2.setIconSize(QtCore.QSize(20, 20))
		
		self.pushButton_3 = QtWidgets.QPushButton(self)
		self.pushButton_3.setGeometry(QtCore.QRect(65, 5, 40, 40))
		self.pushButton_3.setObjectName("pushButton")
		self.pushButton_3.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/redo_system_bar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_3.setIcon(icon)
		self.pushButton_3.setIconSize(QtCore.QSize(20, 20))
		
		self.pushButton_4 = QtWidgets.QPushButton(self)
		self.pushButton_4.setGeometry(QtCore.QRect(103, 15, 20, 20))
		self.pushButton_4.setObjectName("pushButton")
		self.pushButton_4.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_4.setIcon(icon)
		self.pushButton_4.setIconSize(QtCore.QSize(20, 20))
		
		self.pushButton_5 = QtWidgets.QPushButton(self)
		self.pushButton_5.setGeometry(QtCore.QRect(165, 5, 30, 30))
		self.pushButton_5.setObjectName("pushButton")
		self.pushButton_5.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.pushButton_5.setIcon(icon)
		self.pushButton_5.setIconSize(QtCore.QSize(30, 30))
		
		self.label = QtWidgets.QLabel(self)
		self.label.setGeometry(QtCore.QRect(420, 12, 150, 20))
		font = QtGui.QFont()
		font.setFamily("方正粗黑宋简体")
		font.setPointSize(22)

		self.label.setFont(font)
		self.label.setObjectName("label")
		self.label.setText("BrepCAD")
		
		

	def add_ribbon_tab(self, name):
		ribbon_tab = RibbonTab(self, name)
		ribbon_tab.setObjectName("tab_" + name)
		self._ribbon_widget.addTab(ribbon_tab, name)
		return ribbon_tab

	def set_active(self, name):
		self.setCurrentWidget(self.findChild("tab_" + name))