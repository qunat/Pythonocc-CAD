#-*- coding:utf-8 -*-
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension,AIS_LengthDimension,AIS_DiameterDimension,AIS_AngleDimension
from sketcher.sketcher_line import  Brep_line

class Dimension_Manege():
	def __init__(self,parent=None):
		self.parent=parent
		self.Dimension_dict={}
		self.Dimension_list=[]
	
	def Get_Dimension(self,shape):
		#获取尺寸
		pass
	def Set_Dimension(self,shape):
		#设置尺寸
		pass
	def Create_Dimension(self,shape):
		print("Create_Dimension")
		print(shape)
		
		#创建尺寸
		pass
		self.Dimension_dict[1]=AIS_LengthDimension(shape.get_end_point_pnt())
	def Delete_Dimension(self,shape):
		#删除尺寸
		pass
	def Update_Dimension(self,shape):
		#更新尺寸
		pass