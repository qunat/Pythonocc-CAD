# -*- coding: utf-8 -*-
from typing import List

from OCC.Core.AIS import AIS_Trihedron, AIS_Plane, AIS_ViewCube,AIS_Shape
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepTools import breptools_Write, breptools_Read, breptools_Triangulation
from OCC.Core.Geom import Geom_Axis2Placement, Geom_Plane
from OCC.Core.Prs3d import Prs3d_LineAspect
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Shape, TopoDS_Edge, TopoDS_Solid,TopoDS_Shell
from PyQt5.QtWidgets import QFileDialog,QMenu,QWidget
from PyQt5.QtCore import  Qt
from OCC.Extend.DataExchange import read_step_file,read_iges_file,read_stl_file
from Win64.module import Assemble,qtDisplay
from OCC.Core.Quantity import *
from OCC.Core.gp import *
from OCC.Core.Graphic3d import *
from OCC.Core.Select3D import *
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
		DumpToString="PART COMPOUND 0:1:1:1 \"{}\" ".format(name)
		self.DumpToString_list.append(DumpToString)
		code=1

		for i in import_shape:
			if not isinstance(i, TopoDS_Solid):  # 排除非solid
				if "Shell" in str(i):
					DumpToString = "PART SHELL 0:1:1:1:{} \"{}\" ".format(code,"SHELL")
					self.DumpToString_list.append(DumpToString)
					code+=1

				continue
			else:
				DumpToString = "PART SOLID 0:1:1:1:{} \"{}\" ".format(code,"SOLID")
				self.DumpToString_list.append(DumpToString)
				code+=1

		
	def Process(self):
		for j in self.DumpToString_list:
			a=AssembleNode(j)
			if a.struct=="None":
				continue
			self.root_dict[a.order]=(a)
		
			
class DisplayManager(object):
	def __init__(self,parent=None):
		self.canva=qtDisplay.qtViewer3d(parent)
		self.parent=parent
		self.shape_maneger_core_dict={}
		self._select_callbacks=[]
		self.sketcher_maneger_core_dict = {}


		#self.canva.InitDriver()
	
	def SetBackgroundImage(self):
		self.canva._display.SetBackgroundImage("./Images/Pic/Cloudy.png")

	def ProjReferenceAxe(self):#返回当前鼠标位置在视图中的值
		_dragStartPosY = self.canva.dragStartPosY
		_dragStartPosX = self.canva.dragStartPosX
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(_dragStartPosX,
																								   _dragStartPosY)
		if abs(vx)==1:
			x=0
		elif abs(vy)==1:
			y=0
		elif abs(vz)==1 :
			z=0
		return x,y,z,vx, vy, vz

	def Convert(self,point=()):#
		(pixel_x,pixel_y)=self.parent.Displayshape_core.canva._display.View.Convert(point[0],point[1])
		
		return pixel_x,pixel_y
	def Dispalyshape(self):
		self.canva._display.DisplayColoredShape()
		
	def Displaytriehedron(self):
		axis = Geom_Axis2Placement(gp.XOY())
		triehedron = AIS_Trihedron(axis)
		triehedron.SetXAxisColor(Quantity_Color(Quantity_NOC_RED))
		triehedron.SetYAxisColor(Quantity_Color(Quantity_NOC_GREEN))
		triehedron.SetAxisColor(Quantity_Color(Quantity_NOC_BLUE1))
		drawer = triehedron.Attributes()
		self.canva._display.Context.Display(triehedron, 0, 3, True)
		self.shape_maneger_core_dict["axis"]=triehedron
		
		
		
	def Displayplane(self):
		plane = Geom_Plane(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0, 1, 0))
		ais_plane_xz = AIS_Plane(plane, True)
		ais_plane_xz.SetColor(Quantity_Color(Quantity_NOC_GRAY))
		ais_plane_xz.SetTypeOfSensitivity(Select3D_TOS_INTERIOR)
		asp = Prs3d_LineAspect(Quantity_Color(Quantity_NOC_GREEN), 1, 10)
		ais_plane_xz.SetAspect(asp)
		self.canva._display.Context.Display(ais_plane_xz, True)
		self.shape_maneger_core_dict["X基准面"]=ais_plane_xz
		
		plane = Geom_Plane(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(1, 0, 0))
		ais_plane_zy = AIS_Plane(plane, True)
		ais_plane_zy.SetColor(Quantity_Color(Quantity_NOC_WHITE))
		ais_plane_zy.SetTypeOfSensitivity(Select3D_TOS_INTERIOR)
		asp = Prs3d_LineAspect(Quantity_Color(Quantity_NOC_WHITE), 2, 1)
		ais_plane_zy.SetAspect(asp)
		self.canva._display.Context.Display(ais_plane_zy, True)
		self.shape_maneger_core_dict["Y基准面"]=ais_plane_zy
		
		plane = Geom_Plane(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0, 0, 1))
		ais_plane_zy = AIS_Plane(plane, True)
		ais_plane_zy.SetColor(Quantity_Color(Quantity_NOC_WHITE))
		ais_plane_zy.SetTypeOfSensitivity(Select3D_TOS_INTERIOR)
		asp = Prs3d_LineAspect(Quantity_Color(Quantity_NOC_GREEN), 1, 10)
		ais_plane_zy.SetAspect(asp)
		self.canva._display.Context.Display(ais_plane_zy, True)
		self.shape_maneger_core_dict["Z基准面"]=ais_plane_zy
	
	def Displaydatum(self):
		self.Displaytriehedron()
		self.Displayplane()
	
	def select(self):
		pass

	def Hide_datum(self,hide_datum=""):
		if hide_datum!="":
			self.canva._display.Context.Erase(self.shape_maneger_core_dict[hide_datum],True)
			print("345678")
		

	def DisplayCube(self):
		#my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()
		self.shape_maneger_core_dict["cube"] = AIS_ViewCube()
		self.shape_maneger_core_dict["cube"].SetTransformPersistence(Graphic3d_TMF_TriedronPers, gp_Pnt(1, 1, 100))
		self.canva._display.Context.Display(self.shape_maneger_core_dict["cube"], True)

	def HidePart(self,part_name=None):
		try:
			if part_name==None:
				
				self.canva._display.Context.InitDetected()
				shape = self.canva._display.Context.DetectedCurrentShape()  # 通过此方法可以当前鼠标点击的ais_shape

            	#shape = shape.ShapeType();
				ais_shape=AIS_Shape(shape.Reversed())

				for i in self.shape_maneger_core_dict.keys():
					try:
						if self.shape_maneger_core_dict[i].Shape().IsSame(shape.Reversed()) or self.shape_maneger_core_dict[i].Shape().IsPartner(shape.Reversed()):
							self.canva._display.Context.Erase(self.shape_maneger_core_dict[i],True)
							index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
							name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
							self.parent.modeltree_dict[name].tree_root_dict[i].setCheckState(0, Qt.Unchecked)
					except 	Exception as e:
						pass
				self.canva._display.Context.Erase(ais_shape,True)
				
			else:
				self.canva._display.Context.Erase(self.shape_maneger_core_dict[part_name],True)
		except Exception as e:
			pass
	def SetTransparent(self):
		try:
			self.canva._display.Context.InitDetected()
			shape = self.canva._display.Context.DetectedCurrentShape()  # 通过此方法可以当前鼠标点击的ais_shape
			#shape = shape.ShapeType();
			ais_shape=AIS_Shape(shape.Reversed())
			for i in self.shape_maneger_core_dict.keys():
				try:
					if self.shape_maneger_core_dict[i].Shape().IsSame(shape.Reversed()) or self.shape_maneger_core_dict[i].Shape().IsPartner(shape.Reversed()):
						self.shape_maneger_core_dict[i].SetTransparency(0.5)
						self.canva._display.Context.Redisplay(self.shape_maneger_core_dict[i],True,False)
				except 	Exception as e:
					pass
		except Exception as e:
			pass

	def DisplayPart(self,part_name):
		self.canva._display.Context.Display(self.shape_maneger_core_dict[part_name],True)
