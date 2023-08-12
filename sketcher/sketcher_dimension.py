#-*- coding:utf-8 -*-
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension,AIS_LengthDimension,AIS_DiameterDimension,AIS_AngleDimension
from PyQt5.QtWidgets import QTextEdit

from sketcher.sketcher_line import  Brep_line
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d,gp_Ax1

class Dimension_Manege():
	def __init__(self,parent=None):
		self.parent=parent
		self.Dimension_dict={}
		self.Dimension_list=[]
		self.clicked_count=0
		self.dimension_ID=0
		self.text_inner_changed=False
		self.Prs3d_DimensionAspect=None
		self.Prs3d_ArrowAspect=None
		self.arrow_length=1
	
	def setting_Prs3d_DimensionAspect(self,dimension_ID,dimension_alignment=0):
		print("dimension_id",dimension_ID)
		scale=0
		__DimensionAspect = self.Dimension_dict[dimension_ID].DimensionAspect()  # 生成样式类 Prs3d_DimensionAspect
		__ArrowAspect = __DimensionAspect.ArrowAspect()  # 生成箭头的样式类 Prs3d_ArrowAspect
		#设置尺寸对齐方式
		if dimension_alignment==0:
			method=__DimensionAspect.TextHorizontalPosition()
			__DimensionAspect.SetTextHorizontalPosition(3)
		elif dimension_alignment==1:
			method = __DimensionAspect.TextVerticalPosition()
			__DimensionAspect.SetTextVerticalPosition(0)
		#自动调整箭头大小
		if dimension_ID==0:
			text_size=self.Dimension_dict[0].GetValue()
			self.arrow_length=text_size/30
			
		__ArrowAspect.SetLength(self.arrow_length)  # 设置箭头长度
		__DimensionAspect.SetArrowAspect(__ArrowAspect)  # 设置箭头样式
		
		self.Dimension_dict[dimension_ID].SetDimensionAspect(__DimensionAspect)  # 设置 尺寸样式
		
	
	def Create_Dimension(self,shape):
		#创建尺寸
		pass
		shape1=self.parent.parent.Displayshape_core.canva._display.Context.Current( )#通过此方法可以获取尺寸


		print(id(shape1),shape1,AIS_LengthDimension.DownCast(shape1),shape)
		if self.clicked_count==0:
			elements = self.parent.get_all_sketcher_element()
			for element in elements.values():
				if element.ais_shape.Shape().IsEqual(shape[0]):
					self.dimension_element = element
			self.clicked_count += 1
			self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_dimension)
			
		elif self.clicked_count>=1:
			self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_dimension)
			self.parent.parent.Displayshape_core.canva._display.Context.Display(self.Dimension_dict[self.dimension_ID-1], True)
			try:
				_dragStartPosY = self.parent.parent.Displayshape_core.canva.dragStartPosY#获取鼠标点击的位置
				_dragStartPosX = self.parent.parent.Displayshape_core.canva.dragStartPosX#获取鼠标点击的位置
				self.setting_Prs3d_DimensionAspect(self.dimension_ID-1)
				self.text_edit = QTextEdit(self.parent.parent.Displayshape_core.canva)#创建文本框
				dimension_position=self.Dimension_dict[self.dimension_ID-1].GetTextPosition()#获取尺寸的位置
				self.text_edit.setGeometry(_dragStartPosX-30, _dragStartPosY-10, 60, 20)#设置位置和大小
				self.text_edit.setText(str(self.Dimension_dict[self.dimension_ID-1].GetValue()))#设置文本
				self.text_edit.show()
				self.clicked_count=0
				self.dimension_ID = 0
			except Exception as e:
				print(e)
			
	def text_changed(self):
		print("change")
		if self.text_changed=="finish":
			print("finish")
			self.text_edit.close()
			
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
			"尺寸样式设置"
			#__DimensionAspect=self.Dimension_dict[self.dimension_ID].DimensionAspect()#生成样式类 Prs3d_DimensionAspect
			#__ArrowAspect=__DimensionAspect.ArrowAspect ()#生成箭头的样式类 Prs3d_ArrowAspect
			#__ArrowAspect.SetLength(20)#设置箭头长度
			#__DimensionAspect.SetArrowAspect(__ArrowAspect)#设置箭头样式
			#self.Dimension_dict[self.dimension_ID].SetDimensionAspect(__DimensionAspect)#设置 尺寸样式

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