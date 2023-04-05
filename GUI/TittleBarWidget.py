from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from GUI.RibbonTab import RibbonTab
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet
from PyQt5 import  QtWidgets,QtCore,QtGui,Qt

__author__ = 'loujiand'

from GUI.TittleBarButton import TittleBarButton,TittleBarButton_windown

Stylesheet = """
#MainWindow {

    border-radius: 10px;
}
#closeButton {
    min-width: 30px;
    min-height: 30px;
    font-family: "Webdings";
    padding:0px;
   
}
#closeButton:hover {
    color: white;
    background: red;
    border:none;
}
"""


class TittleBarWidget(QToolBar):
	def __init__(self, parent):
		QToolBar.__init__(self, parent)
		self.setStyleSheet(get_stylesheet("ribbon"))
		self.setObjectName("TittleWidget")
		self.setWindowTitle("Tittle")
		self._Tittle_widget = QtWidgets.QWidget(self)
		self._Tittle_widget.setMaximumHeight(37*gui_scale())
		self._Tittle_widget.setMinimumHeight(37*gui_scale())
		self.setMovable(False)
		self.addWidget(self._Tittle_widget)
		self.setStyleSheet("background-color: rgb(14, 162, 185);")
		
		HBOX=QHBoxLayout()
		HBOX_Logo = QHBoxLayout()
		HBOX_Left=QHBoxLayout()
		HBOX_Center = QHBoxLayout()
		HBOX_Right= QHBoxLayout()
		self._Tittle_widget.setLayout(HBOX)
		HBOX.addLayout(HBOX_Logo)
		HBOX.addLayout(HBOX_Left)
		HBOX.addLayout(HBOX_Center,280)
		HBOX.addLayout(HBOX_Right,0)
		#HBOX.setSpacing(500)
		
		#add logo-------------------------------------------------------------------------------------
		#self.logo_pushButton = QtWidgets.QPushButton(self._Tittle_widget)
		#self.logo_pushButton.setObjectName("logo_pushButton")
		
		#self.logo_pushButton.setFlat(True)
		#icon = QtGui.QIcon()
		#icon.addPixmap(QtGui.QPixmap("icons/logo-no-background.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		#self.logo_pushButton.setIcon(icon)
		#self.logo_pushButton.setIconSize(QtCore.QSize(30, 30))
		#HBOX_Logo.addWidget(self.logo_pushButton, 0, QtCore.Qt.AlignVCenter)
		

		#add undo--------------------------------------------------------------------------------------
		self.undo_pushButton = TittleBarButton(self._Tittle_widget)
		self.undo_pushButton.setObjectName("undo_pushButton")
		self.undo_pushButton.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/undo_system_bar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.undo_pushButton.setIcon(icon)
		self.undo_pushButton.setIconSize(QtCore.QSize(20, 20))
		HBOX_Left.addWidget(self.undo_pushButton,0)
		#self.undo_pushButton.setText("撤销")
		
		#add redo---------------------------------------------------------------------------------------------
		self.redo_pushButton = TittleBarButton(self._Tittle_widget)
		self.redo_pushButton.setObjectName("redo_pushButton")
		self.redo_pushButton.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/redo_system_bar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.redo_pushButton.setIcon(icon)
		self.redo_pushButton.setIconSize(QtCore.QSize(20, 20))
		HBOX_Left.addWidget(self.redo_pushButton, 0)
		HBOX_Left.setSpacing(0)
		
		#add save------------------------------------------------------------------------------------------------
		self.save_pushButton = TittleBarButton(self._Tittle_widget)
		self.save_pushButton.setObjectName("save_pushButton")
		self.save_pushButton.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.save_pushButton.setIcon(icon)
		self.save_pushButton.setIconSize(QtCore.QSize(20, 20))
		HBOX_Left.addWidget(self.save_pushButton, 0)

		#---------------------------------------------------------------------------------------------
		self.winwownminimizing_pushButton_5 = TittleBarButton_windown(self._Tittle_widget)
		self.winwownminimizing_pushButton_5.setObjectName("winwownminimizing")
		self.winwownminimizing_pushButton_5.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/winwownminimizing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.winwownminimizing_pushButton_5.setIcon(icon)
		self.winwownminimizing_pushButton_5.setIconSize(QtCore.QSize(10, 10))
		HBOX_Right.addWidget(self.winwownminimizing_pushButton_5, 0, QtCore.Qt.AlignVCenter)
		
		self.windownre_pushButton_5 = TittleBarButton_windown(self._Tittle_widget)
		self.windownre_pushButton_5.setObjectName("windownre")
		self.windownre_pushButton_5.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/windownre.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.windownre_pushButton_5.setIcon(icon)
		self.windownre_pushButton_5.setIconSize(QtCore.QSize(10, 10))
		HBOX_Right.addWidget(self.windownre_pushButton_5, 0, QtCore.Qt.AlignVCenter)
		
		self.exit_pushButton_5 = TittleBarButton_windown(self._Tittle_widget)
		self.exit_pushButton_5.setObjectName("exit_pushButton_5")
		self.exit_pushButton_5.setFlat(True)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/windowclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.exit_pushButton_5.setIcon(icon)
		self.exit_pushButton_5.setIconSize(QtCore.QSize(10, 10))
		HBOX_Right.addWidget(self.exit_pushButton_5, 0, QtCore.Qt.AlignVCenter)
		
		
		self.label = QtWidgets.QLabel(self)
		font = QtGui.QFont()
		font.setFamily("方正粗黑宋简体")
		font.setPointSize(15)

		self.label.setFont(font)
		self.label.setObjectName("label")
		self.label.setText("BrepCAD")
		HBOX_Center.addWidget(self.label, 0, QtCore.Qt.AlignCenter)
		
		

	def add_ribbon_tab(self, name):
		ribbon_tab = RibbonTab(self, name)
		ribbon_tab.setObjectName("tab_" + name)
		self._ribbon_widget.addTab(ribbon_tab, name)
		return ribbon_tab

	def set_active(self, name):
		self.setCurrentWidget(self.findChild("tab_" + name))