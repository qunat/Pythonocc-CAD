# -*- coding: utf-8 -*-


from OCC.Display.qtDisplay import qtViewer3d
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import MainGui
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem, QAbstractItemView,
							 QComboBox, QPushButton, QDockWidget, QListWidget)
from PyQt5.QtGui import QKeySequence as QKSec
from PyQt5.QtGui import QIcon,QBrush
from GUI.RibbonButton import RibbonButton
from GUI.RibbonScrollarea import RibbonScrollarea
from GUI.Icons import get_icon
from GUI.RibbonTextbox import RibbonTextbox
from GUI.RibbonWidget import *
from PyQt5.QtCore import  Qt
from module import DisplayManager,ModelTree


class Auto_create_ribbon(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.ribbon_dict={}
		self.ribbon_table={}  # table 选项
		self._action_dict = {}
		self.ribbon_list = []
		self.panel_dict = {}
		self.Read_ribbon_init()
		self.Create_ribbon()
	def Read_ribbon_init(self):
		with open("./GUI/Ribbon.ini","r",encoding="utf-8") as f:
			inner=f.readlines()
			for i in inner:
				if i=="\t":
					continue
				else:
					i=i.replace("\n","")
					self.ribbon_list.append(i)
	def Create_ribbon(self):
		for ribbon in self.ribbon_list:
			ribbon_list=ribbon.split(" ")
			table_name=ribbon_list[0].split("=")[1]
			panel_name = ribbon_list[1].split("=")[1]
			action_name = ribbon_list[2].split("=")[1]
			icon_name = ribbon_list[3].split("=")[1]
			status_tip = ribbon_list[4].split("=")[1]
			icon_visible = ribbon_list[5].split("=")[1]
			connection = ribbon_list[6].split("=")[1]
			shortcut = ribbon_list[7].split("=")[1]
			if not table_name in self.ribbon_table.keys():
				self.ribbon_table[table_name]=self.parent._ribbon.add_ribbon_tab(table_name) #创建table
			self._action_dict[action_name]=self.add_action(action_name, icon_name, status_tip, True, eval(connection), None)#创建action
			
			if  not table_name in self.ribbon_dict.keys():
				self.panel_dict[panel_name]=self.ribbon_table[table_name].add_ribbon_pane(panel_name)#创建panel
				self.ribbon_dict[table_name]=self.panel_dict.keys()
			else:
				if not panel_name in self.ribbon_dict[table_name]:
					self.panel_dict[panel_name] = self.ribbon_table[table_name].add_ribbon_pane(panel_name)  # 创建panel
					self.ribbon_dict[table_name] = self.panel_dict.keys()
			self.panel_dict[panel_name].add_ribbon_widget(RibbonButton(self.parent, self._action_dict[action_name], True))
		
			
			
	def Set_font(self):
		font = QtGui.QFont()
		font.setFamily("微软雅黑")
		font.setPointSize(12)
		#home_tab.setFont(font)
	
	def add_action(self, caption, icon_name, status_tip, icon_visible, connection, shortcut=None):
		action = QAction(get_icon(icon_name), caption, self.parent)
		action.setStatusTip(status_tip)
		action.triggered.connect(connection)
		action.setIconVisibleInMenu(icon_visible)
		if shortcut is not None:
			action.setShortcuts(shortcut)
		#self.addAction(action)
		return action
	
	
	
	
	
	
class Ui_MainWindow(MainGui.Ui_MainWindow):
	def __init__(self):
		self.setupUi(self)
		self.Displayshape_core=DisplayManager.DisplayManager(self)
		self.modeltree=ModelTree.ModelTree()
		self.setCentralWidget(self.Displayshape_core.canve)
		

		# Ribbon
		self._ribbon = RibbonWidget(self)
		self.addToolBar(self._ribbon)
		self.init_ribbon()
		#ToolBar
		self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		self.insertToolBarBreak(self.toolBar)
		
		
		
		

		# -------------------------------------------------------------------------------------右键单击菜单
		self.menuBar = QtWidgets.QMenuBar(self.centralwidget)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 22))
		self.menuBar.setObjectName("menuBar")
		self.menuasd = QtWidgets.QMenu(self.menuBar)
		self.menuasd.setObjectName("menuasd")
		self.setMenuBar(self.menuBar)
		self.action1123 = QtWidgets.QAction(self)
		self.action1123.setObjectName("action1123")
		self.action654 = QtWidgets.QAction(self)
		self.action654.setObjectName("action654")
		self.action773 = QtWidgets.QAction(self)
		self.action773.setObjectName("action773")
		
		#self.Displayshape_core.canve.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		#self.Displayshape_core.canve.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)

		# -------------      actions   can delete    -----------------
		#self._open_action = self.add_action("Open", "open", "Open file", True, self.on_open_file, QKSec.Open)
		#self._save_action = self.add_action("Save", "save", "Save file", True, self.on_save, QKSec.Save)
		#self._copy_action = self.add_action("Copy", "copy", "Copy selection", True, self.on_copy, QKSec.Copy)
		#self._paste_action = self.add_action("Paste", "paste", "Paste from clipboard", True, self.on_paste, QKSec.Paste)
		#self._zoom_action = self.add_action("Zoom", "zoom", "Zoom in on document", True, self.on_zoom)
		#self._about_action = self.add_action("About", "about", "About QupyRibbon", True, self.on_about)
		#self._license_action = self.add_action("License", "license", "Licence for this software", True, self.on_license)

		# -------------      textboxes     can delete  -----------------

		#self._text_box1 = RibbonTextbox("Text 1", self.on_text_box1_changed, 80)
		#self._text_box2 = RibbonTextbox("Text 2", self.on_text_box1_changed, 80)
		#self._text_box3 = RibbonTextbox("Text 3", self.on_text_box1_changed, 80)


		# 界面布局
		# self.items.setWidget(self)
		# self.setCentralWidget(self.stackedWidget)
		# self.items2.setWidget()
		#左侧模型树
		self.items = QDockWidget('组合浏览器', self)  # 新建QDockWidget
		self.addDockWidget(Qt.LeftDockWidgetArea, self.items)  # 在主显示区域右侧显示
		self.items.setMaximumWidth(400)  # 设置最小大小
		self.items.setWidget(self.modeltree.tree)




	def closeEvent(self, close_event):
		pass

	def on_open_file(self):
		pass
		root_dict=self.Displayshape_core.Open_part()
		try:
			self.modeltree.Create_tree_NodeList(root_dict=root_dict)
		except Exception as e:
			print(e)

	def on_save_to_excel(self):
		pass

	def on_save(self):
		pass

	def on_text_box1_changed(self):
		pass

	def on_text_box2_changed(self):
		pass

	def on_text_box3_changed(self):
		pass

	def on_copy(self):
		pass

	def on_paste(self):
		pass

	def on_zoom(self):
		pass

	def on_about(self):
		text = "QupyRibbon\n"
		text += "This program was made by Magnus Jørgensen.\n"
		text += "Copyright © 2016 Magnus Jørgensen"
		QMessageBox().about(self, "About QupyRibbon", text)

	def on_license(self):
		file = open('LICENSE', 'r')
		lic = file.read()
		QMessageBox().information(self, "License", lic)



	def init_ribbon(self):
		
		
		#------文件选项----------------------------------
		#home_tab = self._ribbon.add_ribbon_tab("文件(F)")#table 选项
		#font = QtGui.QFont()
		#font.setFamily("微软雅黑")
		#font.setPointSize(12)
		#home_tab.setFont(font)
		#file_pane = home_tab.add_ribbon_pane("File")#选项下的菜单
		#file_pane.add_ribbon_widget(RibbonButton(self, self._open_action, True))
		#file_pane.add_ribbon_widget(RibbonButton(self, self._save_action, True))

		#edit_panel = home_tab.add_ribbon_pane("Edit")#选项下的菜单
		#edit_panel.add_ribbon_widget(RibbonButton(self, self._copy_action, True))
		#edit_panel.add_ribbon_widget(RibbonButton(self, self._paste_action, True))

		#grid = edit_panel.add_grid_widget(200)#选项下的菜单
		#grid.addWidget(QLabel("Text box 1"), 1, 1)
		#grid.addWidget(QLabel("Text box 2"), 2, 1)
		#grid.addWidget(QLabel("Text box 3"), 3, 1)
		#grid.addWidget(self._text_box1, 1, 2)
		#grid.addWidget(self._text_box2, 2, 2)
		#grid.addWidget(self._text_box3, 3, 2)
		# test----------------------------------------------
		tab=Auto_create_ribbon(parent=self)
		#tab.Add_panel("打开",None)

		# ------View选项----------------------------------
		#view_panel = home_tab.add_ribbon_pane("View")#选项下的菜单
		#view_panel.add_ribbon_widget(RibbonButton(self, self._zoom_action, True))
		#home_tab.add_spacer()

		# ------工具----------------------------------
		#tool_tab = self._ribbon.add_ribbon_tab("主页")
		#tool_panel = tool_tab.add_ribbon_pane("Info")
		#tool_panel.add_ribbon_widget(RibbonButton(self, self._about_action, True))
		#tool_panel.add_ribbon_widget(RibbonButton(self, self._license_action, True))

		# ------建模----------------------------------
		#fix_tab = self._ribbon.add_ribbon_tab("曲线")
		#fix_panel = fix_tab.add_ribbon_pane("Info")
		#fix_panel.add_ribbon_widget(RibbonButton(self, self._about_action, True))
		#fix_panel.add_ribbon_widget(RibbonButton(self, self._license_action, True))

		# ------其他----------------------------------
		#about_tab = self._ribbon.add_ribbon_tab("其他")
		#info_panel = about_tab.add_ribbon_pane("Info")
		#info_panel.add_ribbon_widget(RibbonButton(self, self._about_action, True))
		#info_panel.add_ribbon_widget(RibbonButton(self, self._license_action, True))

	def rightMenuShow(self):
		try:
			if True:
				rightMenu = QtWidgets.QMenu(self.menuBar)
				self.actionreboot = QtWidgets.QAction(self.canva)
				self.actionreboot.setObjectName("actionreboot")
				self.actionreboot.setText(QtCore.QCoreApplication.translate("MainWindow", "距离测量"))

				self.actionreboot_1 = QtWidgets.QAction(self.canva)
				self.actionreboot_1.setObjectName("actionreboot_1")
				self.actionreboot_1.setText(QtCore.QCoreApplication.translate("MainWindow", "孔径测量"))

				rightMenu.addAction(self.actionreboot)
				rightMenu.addAction(self.actionreboot_1)

				self.actionreboot.triggered.connect(self.Measure_distance_fun)
				self.actionreboot_1.triggered.connect(self.Measure_diameter_fun)

				rightMenu.exec_(QtGui.QCursor.pos())


		except Exception as e:
			print(e)
			pass







