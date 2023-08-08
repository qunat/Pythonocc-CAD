#-*- coding:utf-8 -*-
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension,AIS_LengthDimension,AIS_DiameterDimension,AIS_AngleDimension
from sketcher.sketcher_line import  Brep_line
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d,gp_Ax1

class Dimension_Manege():
	def __init__(self,parent=None):
		self.parent=parent
		self.Dimension_dict={}
		self.Dimension_list=[]
		self.clicked_count=0
		self.dimension_ID=0
	
	def Get_Dimension(self,shape):
		#获取尺寸
		pass
	def Set_Dimension(self,shape):
		#设置尺寸
		pass
	def Create_Dimension(self,shape):
		#创建尺寸
		pass
		print(shape)
		if self.clicked_count==0:
			elements = self.parent.get_all_sketcher_element()
			for element in elements.values():
				if element.ais_shape.Shape().IsEqual(shape[0]):
					self.dimension_element = element
			self.clicked_count += 1
			self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_dimension)
			
		elif self.clicked_count>=1:
			self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_dimension)
			self.parent.parent.Displayshape_core.canva._display.Context.Display(self.Dimension_dict[self.dimension_ID], True)
			self.clicked_count=0
			self.dimension_ID = 0
			
		
	def dynamics_dimension(self):
		if self.clicked_count==1:
			try:
				self.parent.parent.Displayshape_core.canva._display.Context.Remove(
					self.Dimension_dict[self.dimension_ID - 1], True)
			except:
				pass
			(x, y, z, vx, vy, vz) = self.parent.parent.Displayshape_core.ProjReferenceAxe()
			dimension_direction = self.parent.gp_Dir.Rotated(
				gp_Ax1(self.dimension_element.pnt_endpoints_list[0], self.parent.gp_Dir),
				3.14 / 2)
			self.Dimension_dict[self.dimension_ID] = AIS_LengthDimension(self.dimension_element.pnt_endpoints_list[0],
																		 self.dimension_element.pnt_endpoints_list[1],
																		 gp_Pln(gp_Origin(), dimension_direction))
			self.Dimension_dict[self.dimension_ID].SetTextPosition(gp_Pnt(x, y, z))
			self.parent.parent.Displayshape_core.canva._display.Context.Display(self.Dimension_dict[self.dimension_ID],
																				True)
			self.dimension_ID += 1
		
		

		
		
	# 创建尺寸
	def Delete_Dimension(self,shape):
		#删除尺寸
		pass
	def Update_Dimension(self,shape):
		#更新尺寸
		pass