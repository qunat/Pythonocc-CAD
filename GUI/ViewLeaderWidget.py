from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from GUI.RibbonTab import RibbonTab
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet
from PyQt5 import  QtWidgets,QtCore,QtGui,Qt
from PyQt5.QtGui import QPixmap
__author__ = 'loujiand'

from GUI.ViewLeaderButton import ViewLeaderButton,TittleBarButton_windown


class ViewLeaderWidget(QtWidgets.QWidget):
	def __init__(self, parent):
		super(ViewLeaderWidget, self).__init__(parent)
		#self.setStyleSheet(get_stylesheet("ribbon"))
		self.setObjectName("ViewLeaderWidget")
		self.setWindowTitle("前导视图")
		self._ViewLeader_Widget = QtWidgets.QWidget(self)
		self._ViewLeader_Widget.setMaximumHeight(37*gui_scale())
		self._ViewLeader_Widget.setMinimumHeight(37*gui_scale())
		#self.setMovable(False)
		#self.addWidget(self._ViewLeader_Widget)
		HBOX=QHBoxLayout()
		HBOX_Logo = QHBoxLayout()
		HBOX_Left=QHBoxLayout()
		HBOX_Center = QHBoxLayout()
		HBOX_Right= QHBoxLayout()
		self._ViewLeader_Widget.setLayout(HBOX)
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
		
		#add open file
		self.folder_pushButton = ViewLeaderButton(self._ViewLeader_Widget, "folder_pushButton", "folder", [20, 20],"打开")
		HBOX_Left.addWidget(self.folder_pushButton, 0)
		#add undo--------------------------------------------------------------------------------------
		self.undo_pushButton = ViewLeaderButton(self._ViewLeader_Widget,"undo_pushButton","undo_system_bar",[20,20],"撤销")
		HBOX_Left.addWidget(self.undo_pushButton,0)
		#add redo---------------------------------------------------------------------------------------------
		self.redo_pushButton = ViewLeaderButton(self._ViewLeader_Widget,"redo_pushButton","redo_system_bar",[20,20],"重做")
		HBOX_Left.addWidget(self.redo_pushButton, 0)
		#add save------------------------------------------------------------------------------------------------
		self.save_pushButton = ViewLeaderButton(self._ViewLeader_Widget,"save_pushButton","save",[20,20],"保存")
		HBOX_Left.addWidget(self.save_pushButton, 0)
		#add copy
		self.copy_pushButton = ViewLeaderButton(self._ViewLeader_Widget, "copy_pushButton", "copy", [20, 20],"复制")
		HBOX_Left.addWidget(self.copy_pushButton, 0)
		#add paste
		self.paste_pushButton = ViewLeaderButton(self._ViewLeader_Widget, "paste_pushButton", "paste", [20, 20],"黏贴")
		HBOX_Left.addWidget(self.paste_pushButton, 0)
		# add about
		self.about_pushButton = ViewLeaderButton(self._ViewLeader_Widget, "about_pushButton", "about", [20, 20],"关于")
		HBOX_Left.addWidget(self.about_pushButton, 0)
		
		#--------------------------------------------------------------------------------------------------
		#add
		#self.winwownminimizing_pushButton = TittleBarButton_windown(self._ViewLeader_Widget,"winwownminimizing","winwownminimizing",[10,10],)
		#HBOX_Right.addWidget(self.winwownminimizing_pushButton, 0, QtCore.Qt.AlignVCenter)
		#add
		#self.windownre_pushButton = TittleBarButton_windown(self._ViewLeader_Widget,"windownre","windownre",[10,10])
		#HBOX_Right.addWidget(self.windownre_pushButton, 0, QtCore.Qt.AlignVCenter)
		#add
		#self.exit_pushButton = TittleBarButton_windown(self._ViewLeader_Widget,"exit_pushButton_5","windowclose",[10,10])
		#HBOX_Right.addWidget(self.exit_pushButton, 0, QtCore.Qt.AlignVCenter)
		
		print(456)
		self.label = QtWidgets.QLabel(self)
		font = QtGui.QFont()
		font.setFamily("方正粗黑宋简体")
		font.setPointSize(15)

		#self.label.setFont(font)
		#self.label.setObjectName("label")
		#self.label.setText("BrepCAD")
		#HBOX_Center.addWidget(self.label, 0, QtCore.Qt.AlignCenter)
		
		

	def add_ribbon_tab(self, name):
		ribbon_tab = RibbonTab(self, name)
		ribbon_tab.setObjectName("tab_" + name)
		self._ribbon_widget.addTab(ribbon_tab, name)
		return ribbon_tab

	def set_active(self, name):
		self.setCurrentWidget(self.findChild("tab_" + name))