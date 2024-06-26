# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1008, 767)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("./Win64/icons/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		MainWindow.setStyleSheet("")
		MainWindow.setIconSize(QtCore.QSize(160, 128))
		MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setStyleSheet("")
		self.centralwidget.setObjectName("centralwidget")
		self.BrepCADlable=QtWidgets.QLabel(self.centralwidget)
		self.BrepCADlable.setPixmap(QtGui.QPixmap('./Images/pic/BrepCAD2024.png'))
		layout=QtWidgets.QVBoxLayout()
		layout.addWidget(self.BrepCADlable)
		self.centralwidget.setLayout(layout)
		MainWindow.setCentralWidget(self.centralwidget)
		
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		
		#exitAct = QAction(QIcon('./icons/copy.png'), 'Exit', self)
		self.toolBar = QtWidgets.QToolBar("工具栏",MainWindow)
		self.toolBar.setObjectName("toolBar")
		self.toolBar.addSeparator()
		self.toolBar.setIconSize(QtCore.QSize(20, 20))
		#self.toolBar.addAction(exitAct)
		self.statusbar.setStyleSheet("background-color: rgb(45, 93, 135);")
		self.statusbar.setFixedHeight(32)
		#MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		
	

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
	def refreshwindow(self):
		pass


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
