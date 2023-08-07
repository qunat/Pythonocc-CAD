#-*- coding:utf-8 -*-
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension,AIS_LengthDimension,AIS_DiameterDimension,AIS_AngleDimension
from sketcher.sketcher_line import  Brep_line
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d

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
		#创建尺寸
		pass
		elements=self.parent.get_all_sketcher_element()
		for element in elements.values():
			if element.ais_shape.Shape().IsEqual(shape[0]):
				print(element.pnt_endpoints_list[0])
				self.Dimension_dict[1] = AIS_LengthDimension(element.pnt_endpoints_list[0],element.pnt_endpoints_list[1],gp_Pln(gp_Origin(),self.parent.gp_Dir))
				self.parent.parent.Displayshape_core.canva._display.Context.Display(self.Dimension_dict[1],True)
				
			
			
		#self.Dimension_dict[1]=AIS_LengthDimension(shape.get_end_point_pnt())
		print("Create_Dimension")
		print(shape)
	
	# 创建尺寸
	def Delete_Dimension(self,shape):
		#删除尺寸
		pass
	def Update_Dimension(self,shape):
		#更新尺寸
		pass