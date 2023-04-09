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
import re

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
		elif DumpToString_list[0]=="SOLID":
			pass
		elif DumpToString_list[0]=="VERTEX":
			pass
		elif DumpToString_list[0]=="Free":
			pass
		elif DumpToString_list[0]=="FACE":
			pass
		else:
			self.struct=DumpToString_list[0]
			
			self.kind=DumpToString_list[1]
			
			self.order=DumpToString_list[2]
			
			if "(refers" in DumpToString_list[3]:
				self.refer=DumpToString_list[5][0:-1]
				
				pattern = re.compile(r'\"(.*?)\"')
				self.name = pattern.findall(self.DumpToString)[0]
			else:
				pattern = re.compile(r'\"(.*?)\"')
				self.name = pattern.findall(self.DumpToString)[0]
				
			
		#print(self.struct,self.kind,self.order,self.name,self.refer)
			
		
class DumpProcess(object):
	def __init__(self,DumpToString):
		self.root_dict = {}  # {order:AssembleNode}
		self.assembly = []  # {name:order}
		self.prerocess(DumpToString)
	def prerocess(self,DumpToString):
		__DumpToStringstr = str(DumpToString).split("\n")
		__DumpToStringstr=__DumpToStringstr[2:-1]
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
				
				
class NoDumpProcess(object):
	def __init__(self,import_shape=[],file="asm"):
		self.root_dict = {}  # {order:AssembleNode}
		self.DumpToString_list=[]
		self.Create_DumpToString(import_shape,file)
		self.Process()
	def Create_DumpToString(self,import_shape,file):
		try:
			name=file.split("/")[-1].split(".")[0]

		except:
			name = file.split("\\")[-1].split(".")[0]
			
		DumpToString="ASSEMBLY COMPOUND 0:1:1:1 \"{}\" ".format(name)
		self.DumpToString_list.append(DumpToString)
		code=1
		for i in import_shape:
			if not isinstance(i, TopoDS_Solid):  # 排除非solid
				continue
			DumpToString = "PART SOLID 0:1:1:1:{} \"{}\" ".format(code,"SOLID")
			self.DumpToString_list.append(DumpToString)
			code+=1
		#print(self.DumpToString_list)
		
	def Process(self):
		for j in self.DumpToString_list:
			#print(j)
			a=AssembleNode(j)
			if a.struct=="None":
				continue
			self.root_dict[a.order]=(a)
		
			
		
		
	
		
			
class DisplayManager(object):
	def __init__(self,parent=None):
		self.canva=qtDisplay.qtViewer3d(parent)
		self.parent=parent
		self.part_maneger_core_dict={}
		
	def Dispalyshape(self):
		self.canva._display.DisplayColoredShape()

	


