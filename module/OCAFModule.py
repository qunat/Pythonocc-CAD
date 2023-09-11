# -*- coding: utf-8 -*-
import threading
import time,os

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.BRepTools import breptools_Write, breptools_Read, breptools_Triangulation
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Shape, TopoDS_Edge, TopoDS_Solid
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFileDialog, QWidget,QApplication
from module import qtDisplay
from OCC.Extend.DataExchange import read_step_file, read_iges_file, read_stl_file
from module import Assemble, ProcessWidgets
from module.DisplayManager import DumpProcess, NoDumpProcess
from OCC.Core.TopAbs import TopAbs_VERTEX,TopAbs_FACE


def Thread_derocate(fun):
	def decorate():
		# para=(i for i in args)
		t = threading.Thread(target=fun, args=())
		t.start()
	
	return decorate



class OCAF(object):
	def __init__(self, parent=None):
		self.parent = parent
		self.__shape=[]
		pass

	def clicked_callback(self, shp, *kwargs):
		try:
			# print("右键单击有用",shp)
			pass
		except Exception as e:
			print(e)
	
	def Open_part(self):
		try:
			id = 0
			self.parent.Displayshape_core.canva._display.register_select_callback(self.clicked_callback)
			#self.parent.Displayshape_core.canva._display.EraseAll()
			self.parent.modeltree.Clear_tree_NodeList()
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " STP files(*.stp , *.step);;IGES files(*.iges);;STL files(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			if os.path.exists(filepath):
				end_with = str(filepath).lower()
				self.parent.statusbar.showMessage("状态：正在打开，请稍后......")  ###
				Loadprocess=ProcessWidgets.ProcessWidget(self.parent)
				Loadprocess.Show()
				QApplication.processEvents()

				
				# 判断文件类型 选择对应的导入函数
				if end_with.endswith(".step") or end_with.endswith("stp"):#stp格式导入
					self.import_shape, assemble_relation_list, DumpToString = Assemble.read_step_file_with_names_colors(
						filepath)
					print("我主要是看这里",self.import_shape)

					# 判断是否为标准的装配体结构
					
					try:
						root_dict = DumpProcess(DumpToString).root_dict
					except:
						root_dict = NoDumpProcess(self.import_shape.keys(), file=filepath).root_dict
				

					#print("root_dict",root_dict)
					for shpt_lbl_color in self.import_shape:
						
						label, c, property = self.import_shape[shpt_lbl_color]
						# color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
						if not isinstance(shpt_lbl_color, TopoDS_Solid):  # 排除非solid
							continue
						return_shape = self.parent.Displayshape_core.canva._display.DisplayShape(shpt_lbl_color,color=Quantity_Color(c.Red(),c.Green(),c.Blue(),Quantity_TOC_RGB),update=True)
						self.parent.Displayshape_core.shape_maneger_core_dict[id] = return_shape[0]
						id += 1
						QApplication.processEvents()

					# 建立模型树
					print("显示",root_dict)
					try:
						if root_dict != None:
							self.parent.modeltree.Create_tree_NodeList(root_dict=root_dict)
						else:
							pass
					except:
						pass
					
					self.parent.InteractiveOperate.Setting()
					self.parent.statusbar.showMessage("状态：打开成功")  ###
					self.parent.statusBar.showMessage('状态：软件运行正常')
					return root_dict
				
				elif end_with.endswith(".iges") or end_with.endswith(".igs"):#stp格式导入
					import_shape = read_iges_file(filepath)
					self.parent.Displayshape_core.canva._display.DisplayShape(import_shape)
					self.import_shape={import_shape:None}
					root_dict = NoDumpProcess(self.import_shape.keys(), file=filepath).root_dict
					self.parent.modeltree.Create_tree_NodeList(root_dict=root_dict)
					self.parent.statusbar.showMessage("状态：打开成功")  ###
					self.parent.statusBar.showMessage('状态：软件运行正常')
				
				
				elif end_with.endswith(".stl") or end_with.endswith(".stl"):#stl格式导入
					import_shape = read_stl_file(filepath)
					self.parent.Displayshape_core.canva._display.DisplayShape(import_shape)
					self.import_shape={import_shape:None}
					root_dict = NoDumpProcess(self.import_shape.keys(), file=filepath).root_dict
					self.parent.modeltree.Create_tree_NodeList(root_dict=root_dict)
					self.parent.statusbar.showMessage("状态：打开成功")  ###
					self.parent.statusBar.showMessage('状态：软件运行正常')
			
			else:
				self.parent.statusbar.showMessage("错误：文件不存在")  ###
				Loadprocess.Close()

	
		except Exception as e:
			print(e)

		finally:
			Loadprocess.Close()

	
	def Import_part(self):
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '导入文件', './',
															  " STP files(*.stp , *.step);;IGES files(*.iges);;STL files(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			if os.path.exists(filepath):
				end_with = str(filepath).lower()
				self.parent.statusbar.showMessage("状态：正在导入，请稍后......")  ###
				Loadprocess=ProcessWidgets.ProcessWidget(self.parent)
				Loadprocess.Show()
				QApplication.processEvents()

				
				# 判断文件类型 选择对应的导入函数
				if end_with.endswith(".step") or end_with.endswith("stp"):#stp格式导入
					self.import_shape, assemble_relation_list, DumpToString = Assemble.read_step_file_with_names_colors(
						filepath)
					#print(DumpToString)

					# 判断是否为标准的装配体结构
					
					try:
						root_dict = DumpProcess(DumpToString).root_dict
					except:
						root_dict = NoDumpProcess(self.import_shape.keys(), file=filepath).root_dict
						pass
					print("root_dict",root_dict)
					for shpt_lbl_color in self.import_shape:
						
						label, c, property = self.import_shape[shpt_lbl_color]
						# color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
						if not isinstance(shpt_lbl_color, TopoDS_Solid):  # 排除非solid
							continue
						return_shape = self.parent.Displayshape_core.canva._display.DisplayShape(shpt_lbl_color,color=Quantity_Color(c.Red(),c.Green(),c.Blue(),Quantity_TOC_RGB),update=True)
						self.__shape.append(shpt_lbl_color)
						self.parent.Displayshape_core.shape_maneger_core_dict[id] = return_shape[0]
						QApplication.processEvents()

					# 建立模型树
					try:
						if root_dict != None:
							self.parent.modeltree.Create_tree_NodeList(root_dict=root_dict)
						else:
							pass
					except:
						pass
					self.parent.InteractiveOperate.Setting()
					self.parent.statusbar.showMessage("状态：打开成功")  ###
					self.parent.statusBar.showMessage('状态：软件运行正常')

				elif end_with.endswith(".iges") or end_with.endswith(".igs"):#stp格式导入
					import_shape = read_iges_file(filepath)
					self.parent.Displayshape_core.canva._display.DisplayShape(import_shape)
					self.import_shape={import_shape:None}
					root_dict = NoDumpProcess(self.import_shape.keys(), file=filepath).root_dict
					self.parent.modeltree.Create_tree_NodeList(root_dict=root_dict)
					self.parent.statusbar.showMessage("状态：打开成功")  ###
					self.parent.statusBar.showMessage('状态：软件运行正常')
				
				
				elif end_with.endswith(".stl") or end_with.endswith(".stl"):#stl格式导入
					import_shape = read_stl_file(filepath)
					self.__shape.append(import_shape)
					self.parent.Displayshape_core.canva._display.DisplayShape(import_shape)
					self.import_shape={import_shape:None}
					root_dict = NoDumpProcess(self.import_shape.keys(), file=filepath).root_dict
					self.parent.modeltree.Create_tree_NodeList(root_dict=root_dict)
					self.parent.statusbar.showMessage("状态：打开成功")  ###
					self.parent.statusBar.showMessage('状态：软件运行正常')

		except Exception as e:
			print(e)

		finally:
			Loadprocess.Close()
	
	
	def subject(self):
		print(self.__shape)
		try:
			result_shape = BRepAlgoAPI_Cut(self.__shape[0], self.__shape[1]).Shape()
			print(1111,result_shape)
			self.parent.Displayshape_core.canva._display.DisplayShape(result_shape, update=True)
		except Exception as e:
			print(e)
		