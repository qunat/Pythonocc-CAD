# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.gp import gp_Lin
from Win64.module.qtDisplay import qtViewer3d
from PyQt5 import QtCore, QtGui, QtWidgets
from Win64.Gui import MainGui,ModuleSelect
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem, QAbstractItemView,
							 QComboBox, QPushButton, QDockWidget, QListWidget)
from PyQt5.QtGui import QKeySequence as QKSec
from PyQt5.QtGui import QIcon,QBrush
from Win64.Ribbon.RibbonButton import RibbonButton
from Win64.Ribbon.RibbonScrollarea import RibbonScrollarea
from Win64.Ribbon.Icons import get_icon
from Win64.Ribbon.RibbonTextbox import RibbonTextbox
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d
from Win64.Ribbon.RibbonWidget import *
from Win64.Ribbon.TittleBarWidget import *
from Win64.Ribbon.TopBorderBarWidge import *
from Win64.Ribbon.ViewLeaderWidget import *
from PyQt5.QtCore import  Qt
from Win64.module import DisplayManager,ModelTree,OCAFModule,InteractiveModule,ModuleWindowManager,PartOperate
from Win64.sketcher import sketcher
from Win64.surface import swept
from Win64.manufacture import manufacturing
from PyQt5 import QtGui,QtWidgets

class Auto_create_ribbon(object):
	def __init__(self,parent=None,init_name="RibbonMain"):
		self.parent=parent
		self.ribbon_dict={}
		self.ribbon_table={}  # table 选项
		self._action_dict = {}
		self.ribbon_list = []
		self.panel_dict = {}
		self.Read_ribbon_init(init_name)
		self.Create_ribbon()


	def Read_ribbon_init(self,init_name):
		with open("./Win64/Ribbon/{}.ini".format(init_name),"r",encoding="utf-8") as f:
			inner=f.readlines()
			for i in inner:
				if i=="\t":
					continue
				else:
					i=i.replace("\n","")
					self.ribbon_list.append(i)
	def Create_ribbon(self):
		#print(self.parent.moduleselect)
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
			if connection=="None":
				connection="self.void_funtion"
				
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
	
	def add_action(self, caption, icon_name, status_tip, icon_visible, connection, shortcut=None):
		action = QAction(get_icon(icon_name), caption, self.parent)
		action.setStatusTip(status_tip)
		action.triggered.connect(connection)
		action.setIconVisibleInMenu(icon_visible)
		if shortcut is not None:
			action.setShortcuts(shortcut)
		#self.addAction(action)
		return action
	def void_funtion(self):
		pass
	

	
class Ui_MainWindow(MainGui.Ui_MainWindow):
	def __init__(self):
		self.setupUi(self)
		self.setWindowFlags(Qt.FramelessWindowHint)
		#init winwows manager module
		self.ModuleWindowManager=ModuleWindowManager.modulewindowmanager(self)
		#init OCAF module
		self.OCAF=OCAFModule.OCAF(self)
		#init modeltree module
		#self.modeltree=ModelTree.ModelTree()
		#init InteractiveOperate module
		self.InteractiveOperate=InteractiveModule.InteractiveOperate(self)
		#init Sketcher module
		self.Sketcher=sketcher.SketchModule(self)
		#init surface module
		self.Surface=swept.Surface(self)
		#init manufacturing module 
		self.Manufacturing=manufacturing.manufacturing(self)
		#init partoperate module
		self.PartOperate=PartOperate.PartOperate(self)
		


		#Create ModuleSelect
		self.moduleselect=ModuleSelect.moduleselect(self)

		# Create TittleBar
		self.statusBar=QtWidgets.QStatusBar()
		
		
		# Create TittleBar
		self.TittleBar = TittleBarWidget(self)
		self.addToolBar(self.TittleBar)
		#self.init_ribbon()

		
		
		# Create Ribbon
		self._ribbon = RibbonWidget(self)
		self.addToolBar(self._ribbon)
		self.insertToolBarBreak(self._ribbon)
		self.init_ribbon()

		#init parameter
		self.current_window_name=None

		
		
		# Create PythonConsole
		#self.ipython = Ipython.ConsoleWidget(customBanner=None)
		#self.ipython=Ipython.TextBrowser()
		#self.items_ipython = QDockWidget('信息输出控制台', self)  # 新建QDockWidget
		#self.addDockWidget(Qt.BottomDockWidgetArea, self.items_ipython)  # 在主显示区域右侧显示
		#self.items_ipython.setMaximumHeight(180)  # 设置最小大小
		#self.items_ipython.setWidget(self.ipython)
		

	def init_ribbon(self):
		self.RibbonMange=Auto_create_ribbon(parent=self,init_name="RibbonInit")
		self._ribbon._ribbon_widget.setCurrentIndex(0)
	def change_ribbon(self,init_name):
		try:
			self._ribbon._ribbon_widget.clear()
			self.RibbonMange = Auto_create_ribbon(parent=self, init_name=init_name)
			self._ribbon._ribbon_widget.setCurrentIndex(1)
		except:
			pass

	def closeEvent(self, close_event):
		pass

		
	
	
			
		
	def mousePressEvent(self, e):
		if e.buttons() == Qt.LeftButton:
			try:
				self.pos = e.pos()
			except:
				pass
	
	
	def mouseMoveEvent(self, event):
		try:
			if event.buttons() == Qt.LeftButton and self.pos:
				self.move(self.mapToGlobal(event.pos() - self.pos))
			event.accept()
		except:
			pass
			
	





