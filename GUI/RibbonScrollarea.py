from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet

__author__ = 'loujiand'


class RibbonScrollarea(QtWidgets.QScrollArea):
	def __init__(self, parent):
		QtWidgets.QScrollArea.__init__(self, parent)
		self.setStyleSheet(get_stylesheet("ribbonButton"))
		#self.setGeometry(QtCore.QRect(0, 0, 50, 50))
		#self.etWidgetResizable(True)
		#self.setObjectName("scrollArea")
		#self.scrollAreaWidgetContents = QtWidgets.QWidget()
		#self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 107, 67))
		#self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
		#self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		

	def add_ribbon_widget(self, widget):
		self.contentLayout.addWidget(widget, 0, Qt.AlignTop)

	def add_grid_widget(self, width):
		widget = QWidget()
		widget.setMaximumWidth(width)
		grid_layout = QGridLayout()
		widget.setLayout(grid_layout)
		grid_layout.setSpacing(4)
		grid_layout.setContentsMargins(4, 4, 4, 4)
		self.contentLayout.addWidget(widget)
		grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		return grid_layout


class RibbonSeparator(QWidget):
	def __init__(self, parent):
		QWidget.__init__(self, parent)
		self.setMinimumHeight(gui_scale() * 80)
		self.setMaximumHeight(gui_scale() * 80)
		self.setMinimumWidth(1)
		self.setMaximumWidth(1)
		self.setLayout(QHBoxLayout())

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		qp.fillRect(event.rect(), Qt.lightGray)
		qp.end()
