from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from GUI.RibbonTab import RibbonTab
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet
from PyQt5 import  QtWidgets,QtCore,QtGui,Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
__author__ = 'loujiand'

from GUI.ViewLeaderButton import ViewLeaderButton


class ViewLeaderWidget(object):
	def __init__(self, parent):
		#super(ViewLeaderWidget, self).__init__(parent)
		#self.setStyleSheet(get_stylesheet("ribbon"))
		#self.setObjectName("ViewLeaderWidget")
		#self.setWindowTitle("前导视图")
		#self._ViewLeader_Widget = QtWidgets.QWidget(parent)
		#self._ViewLeader_Widget.setMaximumHeight(37*gui_scale())
		#self._ViewLeader_Widget.setMinimumHeight(37*gui_scale())
		#self.setMovable(False)
		#self.addWidget(self._ViewLeader_Widget)
		#self._ViewLeader_Widget.setStyleSheet(get_stylesheet("ViewLeader"))
		self.HBOX=QHBoxLayout()
		HBOX_Logo = QHBoxLayout()
		HBOX_Left=QHBoxLayout()
		HBOX_Center = QHBoxLayout()
		HBOX_Right= QHBoxLayout()
		#parent.TopBorderBasetLayout(self.HBOX)
		self.HBOX.addLayout(HBOX_Logo)
		self.HBOX.addLayout(HBOX_Left)
		self.HBOX.addLayout(HBOX_Center,280)
		self.HBOX.addLayout(HBOX_Right,0)
		self.HBOX.setGeometry(QtCore.QRect(300,0,300,32))
		#HBOX.setSpacing(500)
		#self.setAttribute(Qt.WA_TranslucentBackground)
		
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
		self.folder_pushButton = ViewLeaderButton(parent, "folder_pushButton", "view_top", [32, 32],"打开")
		HBOX_Left.addWidget(self.folder_pushButton, 0)
		#add undo--------------------------------------------------------------------------------------
		self.undo_pushButton = ViewLeaderButton(parent,"undo_pushButton","view_tfr_tri",[32,32],"撤销")
		HBOX_Left.addWidget(self.undo_pushButton,0)
		#add redo---------------------------------------------------------------------------------------------
		self.redo_pushButton = ViewLeaderButton(parent,"redo_pushButton","view_tfr_iso",[32,32],"重做")
		HBOX_Left.addWidget(self.redo_pushButton, 0)
		#add save------------------------------------------------------------------------------------------------
		self.save_pushButton = ViewLeaderButton(parent,"save_pushButton","view_right",[32,32],"保存")
		HBOX_Left.addWidget(self.save_pushButton, 0)
		#add copy
		self.copy_pushButton = ViewLeaderButton(parent, "copy_pushButton", "view_left", [32, 32],"复制")
		HBOX_Left.addWidget(self.copy_pushButton, 0)
		#add paste
		self.paste_pushButton = ViewLeaderButton(parent, "paste_pushButton", "view_front", [32, 32],"黏贴")
		HBOX_Left.addWidget(self.paste_pushButton, 0)
		# add about
		self.about_pushButton = ViewLeaderButton(parent, "about_pushButton", "view_bottom", [32, 32],"关于")
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
		#self.label = QtWidgets.QLabel(self)
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