# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,QDockWidget
from PyQt5 import QtWidgets,QtGui,QtCore
from Win64.module import DisplayManager,ModelTree,PartOperate
from Win64.Ribbon.TopBorderBarWidge import *
from Win64.Ribbon.ViewLeaderWidget import *

class modulewindowmanager(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.items=None
		self.TopBorderBa=None
		# Create a tab widget
		self.tabwidget = QTabWidget(self.parent)
		self.tabwidget.setTabsClosable(True)
		# initial windownname number
		self.modulewindowname_dict={}
		self.parent.Displayshape_core_dict={}
		self.parent.modeltree_dict={}
		self.ViewleaderBar_dict={}
		self.windownname=["零件0"]
		self.windownnum=1
		self.getselectshape=None
		self.tabwidget.currentChanged.connect(self.TabwidgetChangeEvent)



	def CreatePartWindown(self,name=None):
		app = QtWidgets.QApplication.instance()
		if not app:
			app = QtWidgets.QApplication(sys.argv)
		
		if name==None:
			self.CreateWindownname()
		else:
			self.windownname.append(name)

		self.parent.current_window_name=self.windownname[-1]
		# Add tabs to the tab widget
		self.parent.Displayshape_core_dict[self.windownname[-1]]=DisplayManager.DisplayManager(self.parent)
		self.tabwidget.addTab(self.parent.Displayshape_core_dict[self.windownname[-1]].canva, self.windownname[-1])
		self.parent.setCentralWidget(self.tabwidget)
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.InitDriver()
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.qApp = app
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.display_triedron()
		self.parent.Displayshape_core_dict[self.windownname[-1]].Displaydatum()
		self.parent.Displayshape_core_dict[self.windownname[-1]].SetBackgroundImage()
		self.parent.Displayshape_core_dict[self.windownname[-1]].DisplayCube()
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.Repaint()
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.setFocus()
		self.tabwidget.setCurrentIndex(self.tabwidget.count()-1)
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.OnResize()
		self.tabwidget.update()
		self.tabwidget.repaint()
		self.tabwidget.setFocus()
		self.parent.repaint()
		#self.ViewleaderBar_dict[self.windownname[-1]]=ViewLeaderWidget(self.parent.Displayshape_core_dict[self.windownname[-1]].canva)
		
		#change part ribbon 
		if self.items==None and self.TopBorderBa==None:
			self.parent.change_ribbon("RibbonMain")  

		#Create ModelTree
		if self.items==None:
			self.items = QDockWidget('组合浏览器', self.parent)  # 新建QDockWidget
			self.parent.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.items)  # 在主显示区域右侧显示
			self.items.setMinimumWidth(280)# 设置最小大小
		self.parent.modeltree_dict[self.windownname[-1]]=ModelTree.ModelTree(self.parent)
		self.items.setWidget(self.parent.modeltree_dict[self.windownname[-1]].tree)

		#Create TopBorderBar
		if self.TopBorderBa==None:	
			self.TopBorderBa=TopBorderBarWidget(self.parent)
			self.parent.addToolBar(QtCore.Qt.TopToolBarArea, self.TopBorderBa)
			self.parent.insertToolBarBreak(self.TopBorderBa)
		# reset TopBorderBa view
		self.TopBorderBa.reset_triggered_connect()

		#右键单击弹出界面
		self.menuBar = QtWidgets.QMenuBar()
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 606 , 26))
		self.menuBar.setObjectName("menuBar")
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.parent.Displayshape_core_dict[self.windownname[-1]].canva.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)
		#绑定信号和槽
		#self.parent.Displayshape_core_dict[self.windownname[-1]].canva._display.register_select_callback(self.getshape)

		try:
			self.parent.PartOperate.part()

		except Exception as e:
			print(e)
			pass
		

	def CreateWindownname(self):
		number=len(self.windownname)
		if number!=0:
			windownname="零件"+str(number)
			self.windownname.append(windownname)
	def GetWindownName(self):
		index=self.tabwidget.currentIndex()
		name=self.tabwidget.tabText(index)
		return name

	def CreateAssembelyWindown(self):
		pass
	def CreateSheetWindown(self):
		pass
	def TabwidgetChangeEvent(self):
		try:
			index=self.tabwidget.currentIndex()
			name=self.tabwidget.tabText(index)
			self.items.setWidget(self.parent.modeltree_dict[name].tree)
			self.parent.current_window_name=name
			self.TopBorderBa.reset_triggered_connect()
		except:
			pass
	def getshape(self,shp, *kwargs):
		""" This function is called whenever a line is selected
		"""
		for face in shp:
			print(face)

	def rightMenuShow(self):
		try:

			index=self.tabwidget.currentIndex()
			name=self.tabwidget.tabText(index)
			if True:
				self.rightMenu = QtWidgets.QMenu(self.parent)
				self.actionreboot_1 = QtWidgets.QAction("透明",self.parent.Displayshape_core_dict[name].canva)
				self.actionreboot_1.setObjectName("actionreboot_1")
				self.actionreboot_1.setText(QtCore.QCoreApplication.translate("MainWindow", "透明"))
				
				self.actionreboot_2 = QtWidgets.QAction("隐藏",self.parent.Displayshape_core_dict[name].canva)
				self.actionreboot_2.setObjectName("actionreboot_2")
				self.actionreboot_2.setText(QtCore.QCoreApplication.translate("MainWindow", "隐藏"))
				
				self.actionreboot_3 = QtWidgets.QAction("删除",self.parent.Displayshape_core_dict[name].canva)
				self.actionreboot_3.setObjectName("actionreboot_3")
				self.actionreboot_3.setText(QtCore.QCoreApplication.translate("MainWindow", "删除"))

				self.actionreboot_4 = QtWidgets.QAction("属性",self.parent.Displayshape_core_dict[name].canva)
				self.actionreboot_4.setObjectName("actionreboot_4")
				self.actionreboot_4.setText(QtCore.QCoreApplication.translate("MainWindow", "属性"))


				self.actionreboot_1.triggered.connect(self.parent.Displayshape_core_dict[name].SetTransparent)
				self.actionreboot_2.triggered.connect(lambda:self.parent.Displayshape_core_dict[name].HidePart(None))
				
				#self.actionreboot_3.triggered.connect(self.test3)

			
				self.rightMenu.addAction(self.actionreboot_1)
				self.rightMenu.addAction(self.actionreboot_2)
				self.rightMenu.addAction(self.actionreboot_3)
				self.rightMenu.addAction(self.actionreboot_4)
				
				#屏蔽移动时弹出菜单
				if self.parent.Displayshape_core_dict[name].canva.mousemoved==False:
					self.rightMenu.exec_(QtGui.QCursor.pos())
					#self.actionreboot_2.triggered.connect(self.parent.Displayshape_core_dict[name].HidePart())
					
					
		except Exception as e:
		
			pass