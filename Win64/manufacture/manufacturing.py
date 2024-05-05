# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
import threading
import time,re
from OCC.Core.AIS import AIS_Shape
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Pnt,gp_Dir,gp_Circ,gp_Ax2,gp_Lin,gp_Ax1
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCC.Extend.TopologyUtils import TopologyExplorer
from PyQt5.QtWidgets import QHBoxLayout, QDockWidget, \
	QListWidget, QFileDialog
from Win64.manufacture import G_Code_interpreter
from PyQt5 import QtCore, QtWidgets,Qt
from Win64.manufacture.Get_Linear_interpolation import Get_Linear_interpolation_point,Get_Arc_interpolation_point
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge,BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Extend.DataExchange import read_step_file,write_step_file,read_stl_file,read_iges_file,read_step_file_with_names_colors
from OCC.Core.TopoDS import TopoDS_Shape,TopoDS_Builder,TopoDS_Compound,topods_CompSolid
from PyQt5 import QtCore, QtWidgets,Qt
import math


class DialogWidget(QtWidgets.QMainWindow):
	def __init__(self,parent=None):
		super(DialogWidget,self).__init__(parent)
		self.parent = parent
		self.DialogFinish=False
		self.setupUi()
		x = parent.geometry().x() + parent.geometry().width() / 2
		y = parent.geometry().y() + parent.geometry().height() / 2
		self.setGeometry(x, y, 250, 80)
		self.setWindowTitle('创建几何体')
		self.pushbutton_ok.clicked.connect(self.ok)
		self.pushbutton_cancel.clicked.connect(self.cancel)

	
	def setupUi(self):
		self.widget = QtWidgets.QWidget(self)
		self.setCentralWidget(self.widget)
		HBOX = QVBoxLayout()
		HBOX_comboBOX = QVBoxLayout()
		HBOX_text1 = QHBoxLayout()
		HBOX_text2 = QHBoxLayout()
		HBOX_text3 = QHBoxLayout()
		HBOX_button = QHBoxLayout()
		self.widget.setLayout(HBOX)
		HBOX.addLayout(HBOX_comboBOX)
		HBOX.addLayout(HBOX_text1)
		HBOX.addLayout(HBOX_text2)
		HBOX.addLayout(HBOX_text3)
		HBOX.addLayout(HBOX_button)


		#设置combobox
		self.comboBox = QtWidgets.QComboBox(self.widget)
		self.comboBox.setGeometry(QtCore.QRect(80, 100, 221, 500))
		self.comboBox.setObjectName("comboBox")
		self.comboBox.addItem("原点和边长")
		self.comboBox.addItem("两点和高度")
		self.comboBox.addItem("两个对角点")
		HBOX_comboBOX.addWidget(self.comboBox, 0, QtCore.Qt.AlignTop)

		#设置label,text
		self.label1=QtWidgets.QLabel(self.widget)
		self.label1.setText("长度(XC):")
		self.label2 = QtWidgets.QLabel(self.widget)
		self.label2.setText("宽度(YC):")
		self.label3 = QtWidgets.QLabel(self.widget)
		self.label3.setText("高度(ZC):")
		HBOX_text1.addWidget(self.label1)
		HBOX_text2.addWidget(self.label2)
		HBOX_text3.addWidget(self.label3)


		self.text1=QtWidgets.QLineEdit(self.widget)
		self.text1.setMaximumHeight(20)
		self.text2 = QtWidgets.QLineEdit(self.widget)
		self.text2.setMaximumHeight(20)
		self.text3 = QtWidgets.QLineEdit(self.widget)
		self.text3.setMaximumHeight(20)
		HBOX_text1.addWidget(self.text1)
		HBOX_text2.addWidget(self.text2)
		HBOX_text3.addWidget(self.text3)

		self.pushbutton_ok = QtWidgets.QPushButton("确定")
		self.pushbutton_cancel = QtWidgets.QPushButton("取消")
		HBOX_button.addWidget(self.pushbutton_ok)
		HBOX_button.addWidget(self.pushbutton_cancel)
		self.parent.statusBar.showMessage("请设置参数")

	def ok(self):
		self.close()


	def cancel(self):
		self.close()
		self.DialogFinish = True

	def Show(self):
		self.show()



class CreateToolDialog(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(CreateToolDialog, self).__init__(parent)
		self.parent = parent
		self.setupUi()

		x = parent.geometry().x() + parent.geometry().width() / 2
		y = parent.geometry().y() + parent.geometry().height() / 2
		self.setGeometry(x, y, 250, 80)
		self.setWindowTitle('创建几何体')

	# self.pushbutton_ok.clicked.connect(self.ok)
	# self.pushbutton_cancel.clicked.connect(self.cancel)

	def setupUi(self):
		self.widget = QtWidgets.QWidget(self)
		# self.setMovable(False)
		# self.addWidget(self.widget)
		# self.setStyleSheet("background-color: rgb(14, 162, 185);")
		self.setCentralWidget(self.widget)
		HBOX = QVBoxLayout()
		HBOX_comboBOX = QVBoxLayout()
		HBOX_text1 = QHBoxLayout()
		HBOX_text2 = QHBoxLayout()
		HBOX_text3 = QHBoxLayout()
		HBOX_button = QHBoxLayout()
		self.widget.setLayout(HBOX)
		HBOX.addLayout(HBOX_comboBOX)
		HBOX.addLayout(HBOX_text1)
		HBOX.addLayout(HBOX_text2)
		HBOX.addLayout(HBOX_text3)
		HBOX.addLayout(HBOX_button)

		# 设置combobox
		self.comboBox = QtWidgets.QComboBox(self.widget)
		self.comboBox.setGeometry(QtCore.QRect(80, 100, 221, 500))
		self.comboBox.setObjectName("comboBox")
		self.comboBox.addItem("原点和边长")
		self.comboBox.addItem("两点和高度")
		self.comboBox.addItem("两个对角点")
		HBOX_comboBOX.addWidget(self.comboBox, 0, QtCore.Qt.AlignTop)

		# 设置label,text
		self.label1 = QtWidgets.QLabel(self.widget)
		self.label1.setText("长度(XC):")
		self.label2 = QtWidgets.QLabel(self.widget)
		self.label2.setText("宽度(YC):")
		self.label3 = QtWidgets.QLabel(self.widget)
		self.label3.setText("高度(ZC):")
		HBOX_text1.addWidget(self.label1)
		HBOX_text2.addWidget(self.label2)
		HBOX_text3.addWidget(self.label3)

		self.text1 = QtWidgets.QTextEdit(self.widget)
		self.text1.setMaximumHeight(20)
		self.text2 = QtWidgets.QTextEdit(self.widget)
		self.text2.setMaximumHeight(20)
		self.text3 = QtWidgets.QTextEdit(self.widget)
		self.text3.setMaximumHeight(20)
		HBOX_text1.addWidget(self.text1)
		HBOX_text2.addWidget(self.text2)
		HBOX_text3.addWidget(self.text3)

		self.pushbutton_ok = QtWidgets.QPushButton("确定")
		self.pushbutton_cancel = QtWidgets.QPushButton("取消")
		HBOX_button.addWidget(self.pushbutton_ok)
		HBOX_button.addWidget(self.pushbutton_cancel)
		self.parent.statusBar.showMessage("请设置参数")
class manufacturing(object):
	def __init__(self,parent=None):
		pass
		self.parent=parent
		self.pause = 1
		self.interpreter_G_code = G_Code_interpreter.G_code_interpreter()

	def Import_NC_Code(self):  # 导入NC程序
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " NC files(*.nc , *.ngc);;(*.cnc);;(*.prim);;")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			self.interpreter_G_code.Read_nc_code(filepath=filepath)
			file = open(filepath, "r")
			nc_code_list = file.readlines()
			# textBrowser内容清零
			self.parent.ipython.textBrowser.clear()
			self.textBrowser_list = []
			self.parent.statusbar.showMessage('状态：G代码加载中.......')
			
			for i in nc_code_list:
				i = i.strip()
				self.parent.ipython.textBrowser.append(i)
				self.textBrowser_list.append(i)
				QtWidgets.QApplication.processEvents()
			# 返回开头
			self.parent.statusbar.showMessage('状态：G代码加载完成')
			self.parent.ipython.textBrowser.ensureCursorVisible()  # 游标可用
			self.cursor = self.parent.ipython.textBrowser.textCursor()  # 设置游标
			# self.tetxBrowser.moveCursor(self.cursor.setPos(0,0))  # 光标移到最后，这样就会自动显示出来
			self.cursor.setPosition(0)
			self.parent.ipython.textBrowser.setTextCursor(self.cursor)
			QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿
			
		except Exception as e:
			print(e)
			pass

	def Import_machining_part(self):  # 导入加工数据
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			# 判断文件类型 选择对应的导入函数
			end_with = str(filepath).lower()
			if end_with.endswith(".step") or end_with.endswith("stp"):
				self.import_shape = read_step_file(filepath)

			elif end_with.endswith("iges"):
				self.import_shape = read_iges_file(filepath)
			elif end_with.endswith("stl"):
				self.import_shape = read_stl_file(filepath)

			try:
				# self.parent.Displayshape_core.canva._display.Context.Remove(self.show[0], True)
				self.acompound = self.import_shape
				self.show = self.parent.Displayshape_core.canva._display.DisplayShape(self.import_shape, color="WHITE", update=True)
				self.parent.canva._display.FitAll()
			except:
				pass
				# self.show = self.parent.Displayshape_core.canva._display.DisplayShape(self.import_shape, color="WHITE", update=True)
				# self.parent.Displayshape_core.canva._display.FitAll()
				pass
			self.parent.statusbar.showMessage("状态：打开成功")  ###
			self.parent.statusbar.showMessage('状态：软件运行正常')
		except:
			pass

	def Import_machine_model(self):  # 导入机床模型
		pass
		# 清除之前数据
		try:
			try:
				self.Machine_spindle_shape = read_step_file("./manufacture/machine/仿真机床/Machine_spindle.stp")
				self.Machine_work_table = read_step_file("./manufacture/machine/仿真机床/Machine_work_table.stp")
				# self.parent.Displayshape_core.canva._display.Context.Remove(self.show[0], True)
				# self.acompound=self.import_shape
				self.parent.Displayshape_core.canva._display.EraseAll()
				self.parent.Displayshape_core.canva._display.hide_triedron()
				self.parent.Displayshape_core.canva._display.display_triedron()
				self.show_Machine_spindle_shape = self.parent.Displayshape_core.canva._display.DisplayShape(self.Machine_spindle_shape,
																				   color="WHITE", update=True)
				self.show_Machine_work_table = self.parent.Displayshape_core.canva._display.DisplayShape(self.Machine_work_table, color="WHITE",
																				update=True)
				# 主轴移动到安全距离
				self.Axis = gp_Trsf()  # 变换类
				self.Axis.SetTranslation(gp_Vec(0, 0, 50))  # 设置变换类为平移
				self.Axis_Toploc = TopLoc_Location(self.Axis)
				self.parent.Displayshape_core.canva._display.Context.SetLocation(self.show_Machine_spindle_shape[0], self.Axis_Toploc)
				self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				self.parent.Displayshape_core.canva._display.FitAll()
				self.parent.statusbar.showMessage("状态：机床载入成功")  ###
			except:
				pass
			# self.show = self.parent.Displayshape_core.canva._display.DisplayShape(self.import_shape, color="WHITE", update=True)
			# self.parent.Displayshape_core.canva._display.FitAll()

			self.parent.statusbar.showMessage('状态：软件运行正常')
		except:
			pass

	def pause_continun_fun(self):
		self.pause = self.pause * -1
		if self.pause == -1:
			self.pushButton_4.setText("继续")
			self.parent.statusbar.showMessage('状态：仿真暂停')
		else:
			self.pushButton_4.setText("暂停")
			self.parent.statusbar.showMessage('状态：仿真进行中')

	def finish_button_fun(self):
		self.finish = -1
		self.fitall = 1
		self.parent.ipython.textBrowser.ensureCursorVisible()  # 游标可用
		self.cursor = self.parent.ipython.textBrowser.textCursor()  # 设置游标
		# self.tetxBrowser.moveCursor(self.cursor.setPos(0,0))  # 光标移到最后，这样就会自动显示出来
		self.cursor.setPosition(0)
		self.parent.ipython.textBrowser.setTextCursor(self.cursor)
		QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿

	def clear_path_button_fun(self):
		self.clear_path = -1
		self.fitall = 1
		self.parent.Displayshape_core.canva._display.EraseAll()
		self.parent.Displayshape_core.canva._display.hide_triedron()
		self.parent.Displayshape_core.canva._display.display_triedron()
		self.parent.Displayshape_core.canva._display.Repaint()

	def G_code_run_Thread(self):
		t = threading.Thread(target=self.G_code_run, args=[])
		t.start()

	def G_code_run(self):
		# self.textBrowser.ensureCursorVisible()  # 游标可用
		# cursor = self.textBrowser.cursor()  # 设置游标
		self.machining = {"spindle_speed": 0, "feet_speed": 0, "status_G": "G0", "x": 0, "y": 0, "z": 0, "x0": 0,
						  "y0": 0, "z0": 0, "i": 0, "j": 0, "k": 0}
		# new_Create_path=Create_Path()
		self.parent.ipython.textBrowser.clear()
		self.my_cylinder = BRepPrimAPI_MakeCylinder(5.0, 50).Shape()
		self.tool = TopoDS_Shape(self.my_cylinder)  # 建立刀具
		for code, G_Ccode in zip(self.interpreter_G_code.Out_NC_simple, self.textBrowser_list):
			try:
				if self.pause == -1:
					while True:
						QtWidgets.QApplication.processEvents()
						self.parent.statusbar.showMessage('状态：仿真暂停')
						if self.pause == 1 or self.finish == -1 or self.clear_path == -1:
							break
					if self.finish == -1 or self.clear_path == -1:
						self.pushButton_4.setText("暂停")
						break
				# time.sleep(0.02)
				if code == []:
					continue
				print(code)
				# self.textBrowser.append(G_Ccode)

				#self.textBrowser.setTextColor(QtGui.QColor(1, 1, 1))
				self.parent.ipython.textBrowser.append(
					"<font color='red'>" + '{}'.format(code) + "<font>")

				if code[0] == "G01":
					x0 = float(self.machining["x0"])  # 当前X坐标
					y0 = float(self.machining["y0"])  # 当前y坐标
					z0 = float(self.machining["z0"])  # 当前z坐标
					x1 = float(code[1])  # 目标X坐标
					y1 = float(code[2])  # 目标X坐标
					z1 = float(code[3])  # 目标X坐标
					path_pnt_list = Get_Linear_interpolation_point([x0, y0, z0], [x1, y1, z1], step=0.8)
				# print(path_pnt_list)
				elif code[0] == "G00":
					x0 = float(self.machining["x0"])  # 当前X坐标
					y0 = float(self.machining["y0"])  # 当前y坐标
					z0 = float(self.machining["z0"])  # 当前z坐标
					x1 = float(code[1])  # 目标X坐标
					y1 = float(code[2])  # 目标X坐标
					z1 = float(code[3])  # 目标X坐标
					path_pnt_list = [gp_Pnt(x1, y1, z1)]
				# print(path_pnt_list)
				elif code[0] == "G02" or code[0] == "G03":

					x0 = float(self.machining["x0"])  # 当前X坐标
					y0 = float(self.machining["y0"])  # 当前y坐标
					z0 = float(self.machining["z0"])  # 当前z坐标
					x1 = float(code[1])  # 目标X坐标
					y1 = float(code[2])  # 目标y坐标
					z1 = float(code[3])  # 目标z坐标
					i = float(code[4])  # 目标I坐标
					j = float(code[5])  # 目标J坐标
					k = float(code[6])  # 目标K坐标
					path_pnt_list = Get_Arc_interpolation_point([x0, y0, z0], [x1, y1, z1], [i, j, k])
					# self.parent.Displayshape_core.canva._display.DisplayShape(path)
					print("显示成功")
				self.machining["x0"] = x1
				self.machining["y0"] = y1
				self.machining["z0"] = z1

				for path_pnt in path_pnt_list:
					pass
					x = path_pnt.X()
					y = path_pnt.Y()
					z = path_pnt.Z()
					self.Axis_move(distance_x=x, distance_y=y, distance_z=z)
					QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿
					self.parent.statusbar.showMessage('状态：仿真进行中')
				# self.tetxBrowser.moveCursor(self.cursor.setPos(0,0))  # 光标移到最后，这样就会自动显示出来
				# self.cursor.setPosition((self.textBrowser_list.index(code))*60)
				# self.textBrowser.setTextCursor(self.cursor)
				# QtWidgets.QApplication.processEvents()



			except Exception as e:
				print(e)

	def Mill_cut_Simulation(self):
		# self.textBrowser.ensureCursorVisible()  # 游标可用
		# cursor = self.textBrowser.cursor()  # 设置游标
		self.machining = {"spindle_speed": 0, "feet_speed": 0, "status_G": "G0", "x": 0, "y": 0, "z": 0, "x0": 0,
						  "y0": 0, "z0": 0, "i": 0, "j": 0, "k": 0}
		# new_Create_path=Create_Path()
		self.parent.ipython.textBrowser.clear()
		self.my_cylinder = BRepPrimAPI_MakeCylinder(10, 50).Shape()
		self.tool = TopoDS_Shape(self.my_cylinder)  # 建立刀具
		print("开始切削")

		for code, G_Ccode in zip(self.interpreter_G_code.Out_NC_simple, self.textBrowser_list):
			try:
				if self.pause == -1:
					while True:
						QtWidgets.QApplication.processEvents()
						self.parent.statusbar.showMessage('状态：仿真暂停')
						if self.pause == 1 or self.finish == -1 or self.clear_path == -1:
							break
					if self.finish == -1 or self.clear_path == -1:
						#self.pushButton_4.setText("暂停")
						break
				# time.sleep(0.03)
				if code == []:
					continue
				self.parent.ipython.textBrowser.append(G_Ccode)

				G_Ccode = G_Ccode.split(" ")
				print(G_Ccode, )
				start_time = time.time()
				if G_Ccode[0][0] == "G":
					if G_Ccode[0] in ["G00", "G01", "G02", "G03"]:
						self.machining["status_G"] = G_Ccode[0]
				for code in G_Ccode:
					if code[0] == "X":
						self.machining["x"] = code.replace("X", "")
					elif code[0] == "Y":
						self.machining["y"] = code.replace("Y", "")
					elif code[0] == "Z":
						self.machining["z"] = code.replace("Z", "")
					elif code[0] == "I":
						self.machining["i"] = code.replace("I", "")
					elif code[0] == "J":
						self.machining["j"] = code.replace("J", "")
					elif code[0] == "K":
						self.machining["k"] = code.replace("K", "")

				# print(self.machining)
				if self.machining["status_G"] == "G01":
					x0 = float(self.machining["x0"])  # 当前X坐标
					y0 = float(self.machining["y0"])  # 当前y坐标
					z0 = float(self.machining["z0"])  # 当前z坐标
					x1 = float(self.machining["x"])  # 目标X坐标
					y1 = float(self.machining["y"])  # 目标X坐标
					z1 = float(self.machining["z"])  # 目标X坐标
					path_pnt_list = Get_Linear_interpolation_point([x0, y0, z0], [x1, y1, z1], step=2)


				elif self.machining["status_G"] == "G00":
					x0 = float(self.machining["x0"])  # 当前X坐标
					y0 = float(self.machining["y0"])  # 当前y坐标
					z0 = float(self.machining["z0"])  # 当前z坐标
					x1 = float(self.machining["x"])  # 目标X坐标
					y1 = float(self.machining["y"])  # 目标X坐标
					z1 = float(self.machining["z"])  # 目标X坐标
					path_pnt_list = Get_Linear_interpolation_point([x0, y0, z0], [x1, y1, z1], step=1)
				# print(path_pnt_list)
				elif self.machining["status_G"] == "G02" or self.machining["status_G"] == "G03":

					x0 = float(self.machining["x0"])  # 当前X坐标
					y0 = float(self.machining["y0"])  # 当前y坐标
					z0 = float(self.machining["z0"])  # 当前z坐标
					x1 = float(self.machining["x"])  # 目标X坐标
					y1 = float(self.machining["y"])  # 目标X坐标
					z1 = float(self.machining["z"])  # 目标X坐标
					i = float(self.machining["i"])  # 目标I坐标
					j = float(self.machining["j"])  # 目标j坐标
					k = float(self.machining["k"])  # 目标K坐标
					path_pnt_list = Get_Arc_interpolation_point([x0, y0, z0], [x1, y1, z1], [i, j, k],
																Direction=self.machining["status_G"])

				# self.parent.Displayshape_core.canva._display.DisplayShape(path)
				x0 = float(self.machining["x0"])  # 当前X坐标
				y0 = float(self.machining["y0"])  # 当前X坐标
				z0 = float(self.machining["z0"])  # 当前X坐标

				x = float(self.machining["x"])  # 目标X坐标
				y = float(self.machining["y"])  # 目标X坐标
				z = float(self.machining["z"])  # 目标X坐标

				if self.machining["status_G"] in ["G02", "G03", "G01"]:
					# print(path_pnt_list)
					# print(x0,y0,z0,x,y,z)
					self.Create_sweep_tool_path(x0, y0, z0 + self.offset_Z, x, y, z + self.offset_Z)
					pass

				self.machining["x0"] = self.machining["x"]
				self.machining["y0"] = self.machining["y"]
				self.machining["z0"] = self.machining["z"]

				end_time = time.time()
				# print("时间",end_time-start_time)
				for path_pnt_num in range(len(path_pnt_list)):
					pass
					try:
						# print("看这里",path_pnt_num)

						if path_pnt_num == 0:
							continue

						x0 = path_pnt_list[path_pnt_num - 1].X()
						y0 = path_pnt_list[path_pnt_num - 1].Y()
						z0 = path_pnt_list[path_pnt_num - 1].Z()

						x = path_pnt_list[path_pnt_num].X()
						y = path_pnt_list[path_pnt_num].Y()
						z = path_pnt_list[path_pnt_num].Z()
						start_time = time.time()
						if self.machining["status_G"] in ["G02", "G03", "G01"]:
							# self.Create_sweep_tool_path(x0,y0,z0+self.offset_Z,x,y,z+self.offset_Z)
							self.Mill_cut(x, y, z + self.offset_Z)
							self.Create_sweep_tool_path(x0, y0, z0 + self.offset_Z, x, y, z + self.offset_Z)
						else:
							self.Create_sweep_tool_path(x0, y0, z0 + self.offset_Z, x, y, z + self.offset_Z)
							self.Mill_cut(x, y, z + self.offset_Z)

						end_time = time.time()
						# print("时间",end_time-start_time)
						QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿
						self.parent.statusbar.showMessage('状态：仿真进行中')
					# self.tetxBrowser.moveCursor(self.cursor.setPos(0,0))  # 光标移到最后，这样就会自动显示出来
					# self.cursor.setPosition((self.textBrowser_list.index(code))*60)
					# self.textBrowser.setTextCursor(self.cursor)
					# QtWidgets.QApplication.processEvents()
					except    Exception as e:
						print(e)
						pass




			except Exception as e:
				print(e)

	def Axis_move(self, distance_x=None, distance_y=None, distance_z=None):
		pass
		try:
			self.Axis = gp_Trsf()  # 变换类
			self.Axis.SetTranslation(gp_Vec(distance_x, distance_y, distance_z))  # 设置变换类为平移
			self.Axis_Toploc = TopLoc_Location(self.Axis)
			self.tool.Location(self.Axis_Toploc)
			self.parent.Displayshape_core.canva._display.Context.SetLocation(self.show_Machine_spindle_shape[0], self.Axis_Toploc)
			self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		except  Exception as e:
			print(e)

	def Automatic_run(self, distance=[]):
		pass
		self.Mill_cut()

	def Automatic_run_threading(self):
		t = threading.Thread(target=self.Automatic_run, args=[])
		t.start()

	def Create_tool_profile(self, x0, y0, z0, x, y, z, tool_diameter=10, tool_height=30, mode=None):
		# create rectange
		point0 = [0, 0, 0]
		point1 = [0, 0, 0]
		point2 = [0, 0, 0]
		point3 = [0, 0, 0]
		v1 = gp_Vec(gp_Pnt(x0, y0, z0), gp_Pnt(x, y, z));  # 计算两点之间的向量
		v2 = v1.Rotated(gp_Ax1(gp_Pnt(x0, y0, z0), gp_Dir(0, 0, 1)), math.pi / 2)  # 计算向量旋转90度的向量
		v3 = v2.Reversed()  # 计算向量反向的向量
		point0[0] = x0 + tool_diameter / 2 * v2.X()  # 计算矩形的起点
		point0[1] = y0 + tool_diameter / 2 * v2.Y()  # 计算矩形的起个点
		point0[2] = z0 + tool_diameter / 2 * v2.Z()  # 计算矩形的起个点

		point3[0] = x0 + tool_diameter / 2 * v3.X()  # 计算矩形的终点
		point3[1] = y0 + tool_diameter / 2 * v3.Y()  # 计算矩形的起终点
		point3[2] = z0 + tool_diameter / 2 * v3.Z()  # 计算矩形的起终点

		point1[0] = point0[0]
		point1[1] = point0[1]
		point1[2] = point0[2] + tool_height

		point2[0] = point3[0]
		point2[1] = point3[1]
		point2[2] = point3[2] + tool_height

		edge0 = BRepBuilderAPI_MakeEdge(gp_Pnt(point0[0], point0[1], point0[2]),
										gp_Pnt(point1[0], point1[1], point1[2])).Edge()
		edge1 = BRepBuilderAPI_MakeEdge(gp_Pnt(point1[0], point1[1], point1[2]),
										gp_Pnt(point2[0], point2[1], point2[2])).Edge()
		edge2 = BRepBuilderAPI_MakeEdge(gp_Pnt(point2[0], point2[1], point2[2]),
										gp_Pnt(point3[0], point3[1], point3[2])).Edge()
		edge3 = BRepBuilderAPI_MakeEdge(gp_Pnt(point3[0], point3[1], point3[2]),
										gp_Pnt(point0[0], point0[1], point0[2])).Edge()

		rectange = BRepBuilderAPI_MakeWire(edge0, edge1, edge2, edge3).Wire()
		# self.parent.Displayshape_core.canva._display.DisplayShape(rectange)

		return rectange
	
	def Create_sweep_tool_path(self, x0, y0, z0, x, y, z, mode=None):
		# create leading line
		point1 = gp_Pnt(float(x0), float(y0), float(z0))
		point2 = gp_Pnt(float(x), float(y), float(z))
		edge = BRepBuilderAPI_MakeEdge(point1, point2).Edge()
		wire = BRepBuilderAPI_MakeWire(edge).Wire()
		
		ais_shape = AIS_Shape(edge)
		self.parent.Displayshape_core.canva._display.Context.Display(ais_shape, True)
		self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		
		# create profile
		profile_wire = self.Create_tool_profile(x0, y0, z0, x, y, z)
		profile_face = BRepBuilderAPI_MakeFace(profile_wire).Face()
		self.pipe = BRepOffsetAPI_MakePipe(wire, profile_face).Shape()
		# ais_shape=AIS_Shape(self.pipe)
		# self.parent.Displayshape_core.canva._display.Context.Display(ais_shape,True)
		return self.pipe
	
	def Mill_cut(self, x=0, y=0, z=0):
		try:
			self.Axis_move(distance_x=x, distance_y=y, distance_z=z)
			Cutting_result = BRepAlgoAPI_Cut(self.Blank, self.tool)
			Cutting_result.SimplifyResult()
			self.Blank = Cutting_result.Shape()
			self.show_Blank[0].SetShape(self.Blank)  # 将已经显示的零件设置成另外一个新零件
			self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_Blank[0], True,
																		   False)  # 重新计算更新已经显示的物体
		except Exception as e:
			pass
			print(e)
			self.parent.statusbar.showMessage('错误：请确认机床组件已经导入')
	
	def Create_Blank(self):
		def func():
			L = float(Blank_dialog.text1.text())
			W = float(Blank_dialog.text2.text())
			H = float(Blank_dialog.text3.text())
			self.Blank = BRepPrimAPI_MakeBox(L, W, H).Shape()
			self.Blank = TopoDS_Shape(self.Blank)
			T = gp_Trsf()
			location_X = -L / 2
			location_Y = -W / 2
			T.SetTranslation(gp_Vec(location_X, location_Y, 0))
			loc = TopLoc_Location(T)
			self.Blank.Location(loc)
			self.show_Blank = self.parent.Displayshape_core.canva._display.DisplayShape(self.Blank, transparency=0.5,
																						update=True)
			change = self.show_Blank[0].Shape()
			self.offset_Z = H
			print(self.offset_Z)

		try:
			Blank_dialog=DialogWidget(self.parent)
			Blank_dialog.show()
			Blank_dialog.pushbutton_ok.clicked.connect(func)
		except Exception as e:
			print(e)
	
	def Delete_Blank(self):
		try:
			# self.parent.Displayshape_core.canva._display.Context.Remove(self.show_Blank[0],True)
			# self.lineEdit_8.clear()
			# self.lineEdit_9.clear()
			# self.lineEdit_10.clear()
			t1 = time.time()
			# self.parent.Displayshape_core.canva._display.Context.Erase(self.show_Blank[0], True)
			# self.parent.Displayshape_core.canva._display.Context.Remove(self.show_Blank[0],True)
			t2 = time.time()
			print(t2 - t1)
			
			box = BRepPrimAPI_MakeBox(float(self.lineEdit_8.text()), float(self.lineEdit_9.text()),
									  float(self.lineEdit_10.text())).Shape()
			# Fillet
			fillet = BRepFilletAPI_MakeFillet(box)
			for e in TopologyExplorer(box).edges():
				fillet.Add(20, e)
			blended_box = ((fillet.Shape()))
			self.show_Blank[0].SetShape(blended_box)  # 将已经显示的零件设置成另外一个新零件
			self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_Blank[0], True,
																		   False)  # 重新计算更新已经显示的物体
			self.parent.Displayshape_core.canva._display.FitAll()
		# self.parent.Displayshape_core.canva._display.Repaint()
		
		except Exception as e:
			print(e)
			pass
