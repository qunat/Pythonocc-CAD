# -*- coding: utf-8 -*-
from typing import List

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Write, breptools_Read, breptools_Triangulation
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Shape, TopoDS_Edge, TopoDS_Solid
from PyQt5.QtWidgets import QFileDialog
from module import qtDisplay
from OCC.Extend.DataExchange import read_step_file,read_iges_file,read_stl_file
from module import Assemble

class AssembleNode(object):
	def __init__(self,DumpToString):
		pass
		self.DumpToString=DumpToString
		self.struct=None
		self.kind=None
		self.order=None
		self.name=None
		self.refer=None
		self.Process()
	def Process(self):
		DumpToString_list=self.DumpToString.split(" ")
		if DumpToString_list[0]=="EDGE":
			pass
		elif DumpToString_list[0]=="Free":
			pass
		else:
			self.struct=DumpToString_list[0]
			self.kind=DumpToString_list[1]
			self.order=DumpToString_list[2]
			if "(refers" in DumpToString_list[3]:
				self.refer=DumpToString_list[5][0:-1]
				if "=>[" in DumpToString_list[6]:
					self.name=DumpToString_list[6]
				else:
					self.name=DumpToString_list[6]
			else:
				self.name = DumpToString_list[3].replace('"',"")
			
		print(self.struct,self.kind,self.order,self.name,self.refer)
			
		
class DumpProcess(object):
	def __init__(self,DumpToString):
		self.root_dict = {}  # {order:AssembleNode}
		self.assembly = []  # {name:order}
		self.prerocess(DumpToString)
		
	def prerocess(self,DumpToString):
		__DumpToStringstr = str(DumpToString).split("\n")
		__DumpToStringstr=__DumpToStringstr[2:-1]
		#print(__DumpToStringstr)
		self.DumpToString=[]
		for compenant in __DumpToStringstr:
			if compenant=="":
				self.assembly.append(self.DumpToString)
				self.DumpToString = []
				continue
			if "\t" in compenant:
				compenant=compenant.replace("\t","")
			self.DumpToString.append(compenant)
		for i in self.assembly:
			for j in i:
				a=AssembleNode(j)
				if a.struct=="None":
					continue
				self.root_dict[a.order]=(a)
				
			
			
	
				
				


class DisplayManager(object):
	def __init__(self,parent=None):
		self.canve=qtDisplay.qtViewer3d(parent)
		self.parent=parent
		self.part_maneger_core_dict={}
		
	def Dispalyshape(self):
		self.canve._display.DisplayColoredShape()

	def Open_part(self):
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			# 判断文件类型 选择对应的导入函数
			end_with = str(filepath).lower()
			if end_with.endswith(".step") or end_with.endswith("stp"):
				self.import_shape,assemble_relation_list,DumpToString =Assemble.read_step_file_with_names_colors(filepath)
				print(DumpToString)
				root_dict=DumpProcess(DumpToString).root_dict
						
				
				for shpt_lbl_color in self.import_shape:
					label, c,property= self.import_shape[shpt_lbl_color]
					#color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
					if  not isinstance(shpt_lbl_color,TopoDS_Solid):#排除非solid
						continue
					return_shape=self.canve._display.DisplayShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
																					 c.Green(),
																					 c.Blue(),
																					 Quantity_TOC_RGB))
					self.part_maneger_core_dict[label]=return_shape
				self.parent.statusbar.showMessage("状态：打开成功")  ###
				self.parent.statusBar().showMessage('状态：软件运行正常')
				return root_dict
			elif end_with.endswith(".iges") or end_with.endswith(".igs"):
				self.import_shape = read_iges_file(filepath)
				self.parent.statusbar.showMessage("状态：打开成功")  ###
				self.parent.statusBar().showMessage('状态：软件运行正常')
			elif end_with.endswith(".stl") or end_with.endswith(".stl"):
				self.import_shape = read_stl_file(filepath)
				breptools_Triangulation()
				breptools_Write(self.import_shape, 'box.brep')
				read_box = TopoDS_Shape()
				builder = BRep_Builder()
				breptools_Read(read_box, 'box.brep', builder)
				self.canve._display.DisplayShape(read_box)
				self.parent.statusbar.showMessage("状态：打开成功")  ###
				self.parent.statusBar().showMessage('状态：软件运行正常')

		except Exception as e:
			print(e)

	def Import_stp(self):
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			# 判断文件类型 选择对应的导入函数
			end_with = str(filepath).lower()
			if end_with.endswith(".step") or end_with.endswith("stp"):
				self.import_shape,assemble_relation_list =Assemble.read_step_file_with_names_colors(filepath)
				for shpt_lbl_color in self.import_shape:
					label, c,property= self.import_shape[shpt_lbl_color]
					#color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
					return_shape=self.canve._display.DisplayShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
																					 c.Green(),
																					 c.Blue(),
																					 Quantity_TOC_RGB))
					self.part_maneger_core_dict[label]=return_shape
			print(self.part_maneger_core_dict)
			self.parent.statusbar.showMessage("状态：打开成功")  ###
			self.parent.statusBar().showMessage('状态：软件运行正常')
			return assemble_relation_list
		except Exception as e:
			print(e)
			
	def Import_iges(self):
		pass
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			# 判断文件类型 选择对应的导入函数
			end_with = str(filepath).lower()
			if end_with.endswith("iges"):
				self.import_shape = read_iges_file(filepath)
			self.parent.statusbar.showMessage("状态：打开成功")  ###
			self.parent.statusBar().showMessage('状态：软件运行正常')

		except:
			pass
	def Import_stl(self):
		try:
			self.chose_document = QFileDialog.getOpenFileName(self.parent, '打开文件', './',
															  " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
			filepath = self.chose_document[0]  # 获取打开文件夹路径
			# 判断文件类型 选择对应的导入函数
			end_with = str(filepath).lower()
			if end_with.endswith("stl"):
				self.import_shape = read_stl_file(filepath)
			self.parent.statusbar.showMessage("状态：打开成功")  ###
			self.parent.statusBar().showMessage('状态：软件运行正常')
		except:
			pass


