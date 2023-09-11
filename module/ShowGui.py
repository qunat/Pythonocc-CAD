# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.gp import gp_Lin
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
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d
from GUI.RibbonWidget import *
from GUI.TittleBarWidget import *
from GUI.TopBorderBarWidge import *
from PyQt5.QtCore import  Qt
from module import DisplayManager,ModelTree,OCAFModule,InteractiveModule#,Ipython
from sketcher import sketcher
from PyQt5 import QtGui,QtWidgets

class Auto_create_ribbon(object):
	def __init__(self,parent=None,init_name="Ribbon_main"):
		self.parent=parent
		self.ribbon_dict={}
		self.ribbon_table={}  # table 选项
		self._action_dict = {}
		self.ribbon_list = []
		self.panel_dict = {}
		self.Read_ribbon_init(init_name)
		self.Create_ribbon()
	def Read_ribbon_init(self,init_name):
		with open("./GUI/{}.ini".format(init_name),"r",encoding="utf-8") as f:
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
		self.Displayshape_core=DisplayManager.DisplayManager(self)
		self.OCAF=OCAFModule.OCAF(self)
		self.modeltree=ModelTree.ModelTree()
		self.InteractiveOperate=InteractiveModule.InteractiveOperate(self)
		self.Sketcher=sketcher.SketchModule(self)
		self.setCentralWidget(self.Displayshape_core.canva)

		
		# Create TittleBar
		self.TittleBar = TittleBarWidget(self)
		self.addToolBar(self.TittleBar)
		#self.init_ribbon()
		
		# Create Ribbon
		self._ribbon = RibbonWidget(self)
		self.addToolBar(self._ribbon)
		self.insertToolBarBreak(self._ribbon)
		self.init_ribbon()
		
		#Create TopBorderBar
		self.TopBorderBa=TopBorderBarWidget(self)
		self.addToolBar(QtCore.Qt.TopToolBarArea, self.TopBorderBa)
		self.insertToolBarBreak(self.TopBorderBa)
		#exitAct = QAction(QIcon('./icons/copy.png'), 'Exit', self)
		#self.toolBar.addAction(exitAct)
		
		
		#右键单击弹出界面
		self.menuBar = QtWidgets.QMenuBar()
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 606 , 26))
		self.menuBar.setObjectName("menuBar")
		#self.Displayshape_core.canva.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		#self.Displayshape_core.canva.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)
		#self.Displayshape_core.canva.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		#self.Displayshape_core.canva.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)
		
		#Create ModelTree
		self.items = QDockWidget('组合浏览器', self)  # 新建QDockWidget
		self.addDockWidget(Qt.LeftDockWidgetArea, self.items)  # 在主显示区域右侧显示
		self.items.setMinimumWidth(350)# 设置最小大小
		self.items.setWidget(self.modeltree.tree)
		
		# Create PythonConsole
		#self.ipython = Ipython.ConsoleWidget(customBanner=None)
		#self.items_ipython = QDockWidget('PythonConsole', self)  # 新建QDockWidget
		#self.addDockWidget(Qt.BottomDockWidgetArea, self.items_ipython)  # 在主显示区域右侧显示
		#self.items_ipython.setMaximumHeight(150)  # 设置最小大小
		#self.items_ipython.setWidget(self.ipython)
		

	def closeEvent(self, close_event):
		pass

	def init_ribbon(self):
		self.RibbonMange=Auto_create_ribbon(parent=self,init_name="Ribbon_main")
		self._ribbon._ribbon_widget.setCurrentIndex(1)
	def change_ribbon(self,init_name):
		try:
			self._ribbon._ribbon_widget.clear()
			self.RibbonMange = Auto_create_ribbon(parent=self, init_name=init_name)
			
		except:
			pass
		
		
	def rightMenuShow(self):
		try:
			if True:
				rightMenu = QtWidgets.QMenu(self.menuBar)
				self.actionreboot_1 = QtWidgets.QAction(self.Displayshape_core.canva)
				self.actionreboot_1.setObjectName("actionreboot_1")
				self.actionreboot_1.setText(QtCore.QCoreApplication.translate("MainWindow", "从列表中选择"))
				
				self.actionreboot_2 = QtWidgets.QAction(self.Displayshape_core.canva)
				self.actionreboot_2.setObjectName("actionreboot_2")
				self.actionreboot_2.setText(QtCore.QCoreApplication.translate("MainWindow", "隐藏"))
				
				self.actionreboot_3 = QtWidgets.QAction(self.Displayshape_core.canva)
				self.actionreboot_3.setObjectName("actionreboot_2")
				self.actionreboot_3.setText(QtCore.QCoreApplication.translate("MainWindow", "删除"))

				self.actionreboot_4 = QtWidgets.QAction(self.Displayshape_core.canva)
				self.actionreboot_4.setObjectName("actionreboot_4")
				self.actionreboot_4.setText(QtCore.QCoreApplication.translate("MainWindow", "属性"))

				
				rightMenu.addAction(self.actionreboot_1)
				rightMenu.addAction(self.actionreboot_2)
				rightMenu.addAction(self.actionreboot_3)
				rightMenu.addAction(self.actionreboot_4)

				self.actionreboot_2.triggered.connect(self.hide_part_rightMenuShow)
				#self.actionreboot_1.triggered.connect(self.Measure_diameter_fun)
				rightMenu.exec_(QtGui.QCursor.pos())

		except Exception as e:
			print(e)
			pass
	def hide_part_rightMenuShow(self):
		Distance=0
		min_distance_id=0
		(x, y, z, vx, vy, vz) = self.Displayshape_core.ProjReferenceAxe()
		direction = gp_Dir(vx, vy, vz)
		line = gp_Lin(gp_Pnt(x, y, z), direction)
		edge_builder = BRepBuilderAPI_MakeEdge(line)
		edge = edge_builder.Edge()
		#print(self.Displayshape_core.shape_maneger_core_dict)
		for key in self.Displayshape_core.shape_maneger_core_dict.keys():
			try:
				#print(key)
				extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.Displayshape_core.shape_maneger_core_dict[key].Shape(), edge)
				nearest_point1 = extrema.PointOnShape1(1)
				nearest_point2 = extrema.PointOnShape2(1)
				if  nearest_point1.Distance(nearest_point2)== 0:
					Distance = nearest_point1.Distance(nearest_point2)
					min_distance_id=key
		
			except:
				pass
		self.Displayshape_core.canva._display.Context.Erase(self.Displayshape_core.shape_maneger_core_dict[min_distance_id],True)
		print(min_distance_id)
			
		
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
			
	





