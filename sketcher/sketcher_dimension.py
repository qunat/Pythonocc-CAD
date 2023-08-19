#-*- coding:utf-8 -*-
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Circ, gp_Pnt
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension,AIS_LengthDimension,AIS_DiameterDimension,AIS_AngleDimension
from PyQt5.QtWidgets import QTextEdit, QLineEdit

from sketcher.sketcher_line import  Brep_line
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d,gp_Ax1
import functools
class Dimension_Manege():
	def __init__(self,parent=None):
		self.parent=parent
		self.Dimension_dict={}
		self.Dimension_list=[]
		self.clicked_count=0
		self.dimension_ID=0
		self.selected_dimension=None
		self.text_inner_changed=False
		self.Prs3d_DimensionAspect=None
		self.Prs3d_ArrowAspect=None
		self.arrow_length=1
		self.text_height=1
		self.text_size=1
		self.parent.parent.Displayshape_core.canva.keyPressEvent_Signal.trigger.connect(self.dimension_changed)
		self.parent.parent.Displayshape_core.canva.mousePressEvent_Signal.trigger.connect(self.drag_dimension)
		self.parent.parent.Displayshape_core.canva.mouseDoubleClickEvent_Signal.trigger.connect(self.edit_dimension)
		
	
	def setting_Prs3d_DimensionAspect(self,dimension_ID=0,dimension_alignment=0):
	
		__DimensionAspect = self.Dimension_dict[dimension_ID].DimensionAspect()  # 生成样式类 Prs3d_DimensionAspect
		__ArrowAspect = __DimensionAspect.ArrowAspect()  # 生成箭头的样式类 Prs3d_ArrowAspect
		__TextAspect = __DimensionAspect.TextAspect()  # 生成文字的样式类 Prs3d_TextAspect
		# 设置尺寸对齐方式
		if dimension_alignment == 0:
			method = __DimensionAspect.TextHorizontalPosition()
			__DimensionAspect.SetTextHorizontalPosition(3)
		elif dimension_alignment == 1:
			method = __DimensionAspect.TextVerticalPosition()
			__DimensionAspect.SetTextVerticalPosition(0)
			
		# 自动调整箭头大小/文本高度
		if len(self.Dimension_dict.keys()) == 1 :#如果是第一次创建尺寸
				self.text_size = self.Dimension_dict[dimension_ID].GetValue()
				if self.text_size < 1400:
					self.arrow_length = 4*5*1.5
					self.text_height =10*1.5
					__TextAspect.SetHeight(self.text_height)
		
			
	
		__ArrowAspect.SetLength(self.arrow_length * (1 / self.parent.parent.Displayshape_core.canva.scaling_ratio))  # 设置箭头长度
		__TextAspect.SetHeight(self.text_height)  # 设置文字高度
		__DimensionAspect.SetArrowAspect(__ArrowAspect)  # 设置箭头样式
		__DimensionAspect.SetTextAspect(__TextAspect)  # 设置文字样式
		

		self.Dimension_dict[dimension_ID].SetDimensionAspect(__DimensionAspect)  # 设置尺寸样式
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(5, 1, True)  # 更新所有尺寸显示

		
		
	def Create_Dimension(self,shape):

		# 创建尺寸
		if self.clicked_count==0:
			elements = self.parent.get_all_sketcher_element()
			for element in elements.keys():
				if elements[element].ais_shape.Shape().IsEqual(shape[0]):
					self.dimension_element =elements[element]
					self.dimension_ID=element
			self.clicked_count += 1
			self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_dimension)
			
			
		elif self.clicked_count>=1:
			self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_dimension)
			try:
				_dragStartPosY = self.parent.parent.Displayshape_core.canva.dragStartPosY#获取鼠标点击的位置
				_dragStartPosX = self.parent.parent.Displayshape_core.canva.dragStartPosX#获取鼠标点击的位置
				self.setting_Prs3d_DimensionAspect(self.dimension_ID,0)
				self.parent.parent.Displayshape_core.canva._display.Context.Display(self.Dimension_dict[self.dimension_ID], True)
				self.line_edit = QLineEdit(self.parent.parent.Displayshape_core.canva)#创建文本框
				self.line_edit.setGeometry(_dragStartPosX-30, _dragStartPosY-10, 60, 20)#设置位置和大小
				self.line_edit.setText(str("{:.2f}".format(self.Dimension_dict[self.dimension_ID].GetValue())))#设置文本
				self.line_edit.show()
				self.clicked_count=0
				self.parent.parent.Displayshape_core.canva.wheelEvent_Signal.trigger.connect(functools.partial(self.setting_Prs3d_DimensionAspect,self.dimension_ID,0))
			except Exception as e:
				print(e)

	def dynamics_dimension(self):
		if self.clicked_count == 1:
			if self.dimension_ID not in self.Dimension_dict.keys():
				(x, y, z, vx, vy, vz) = self.parent.parent.Displayshape_core.ProjReferenceAxe()
				dimension_direction = self.parent.gp_Dir.Rotated(
					gp_Ax1(self.dimension_element.pnt_endpoints_list[0], self.parent.gp_Dir), 3.14 / 2)
				self.Dimension_dict[self.dimension_ID] = AIS_LengthDimension(
					self.dimension_element.pnt_endpoints_list[0], self.dimension_element.pnt_endpoints_list[1],
					gp_Pln(gp_Origin(), dimension_direction))
				self.Dimension_dict[self.dimension_ID].SetTextPosition(gp_Pnt(x, y, z))
				self.setting_Prs3d_DimensionAspect(self.dimension_ID, 0)
				self.parent.parent.Displayshape_core.canva._display.Context.Display(
					self.Dimension_dict[self.dimension_ID], True)
			else:
				(x, y, z, vx, vy, vz) = self.parent.parent.Displayshape_core.ProjReferenceAxe()
				self.Dimension_dict[self.dimension_ID].SetTextPosition(gp_Pnt(x, y, z))
				self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(5, 1, True)
				self.parent.parent.Displayshape_core.canva._display.Repaint()
				
			
			
			
	
	def dimension_changed(self):
		if self.selected_dimension==None:#第一次创建尺寸的回车事件
			(x, y, z, vx, vy, vz) = self.parent.parent.Displayshape_core.ProjReferenceAxe()
			self.Dimension_dict[self.dimension_ID].SetCustomValue(float(self.line_edit.text()))
			self.Dimension_dict[self.dimension_ID].SetTextPosition(gp_Pnt(x, y, z))
		else:#修改尺寸的回车事件
			self.selected_dimension.SetCustomValue(float(self.line_edit.text()))
			self.selected_dimension=None
			
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(5, 1, True)
		self.line_edit.close()
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		
	def edit_dimension(self):#双击修改尺寸数值
		#_dragStartPosY = self.parent.parent.Displayshape_core.canva.dragStartPosY  # 获取鼠标点击的位置
		#_dragStartPosX = self.parent.parent.Displayshape_core.canva.dragStartPosX  # 获取鼠标点击的位置
		
		try:
			dimension_shape = self.parent.parent.Displayshape_core.canva._display.Context.Current()  # 通过此方法可以获取尺寸
			dimension = AIS_LengthDimension.DownCast(dimension_shape)
			position = dimension.GetTextPosition()
			self.selected_dimension=dimension
			self.line_edit = QLineEdit(self.parent.parent.Displayshape_core.canva)  # 创建文本框
			(xp,yp)=self.parent.parent.Displayshape_core.Convert(position.Coord())#将三维点变成像素点
			self.line_edit.setGeometry(xp-30, yp-10, 60, 20)  # 设置位置和大小
			self.line_edit.show()
			self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(5, 1, True)
			self.parent.parent.Displayshape_core.canva._display.Repaint()
		except Exception as e:
			print(e)
			
		
	
	def move_dimension(self):
		(x, y, z, vx, vy, vz) = self.parent.parent.Displayshape_core.ProjReferenceAxe()
		self.Dimension_dict[self.selected_dimension_ID].SetTextPosition(gp_Pnt(x, y, z))
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(5, 1, True)
		self.parent.parent.Displayshape_core.canva._display.Repaint()
	def move_dimension_end(self):
		self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.move_dimension)
		self.parent.parent.Displayshape_core.canva.mouseReleaseEvent_Signal.trigger.disconnect(self.move_dimension_end)
	def drag_dimension(self):
		# 拖动/重新设置尺寸数值IsEqual()
		try:
			#dimension_shape = self.parent.parent.Displayshape_core.canva._display.Context.SelectedInteractive() # 通过此方法可以获取尺寸
			dimension_shape = self.parent.parent.Displayshape_core.canva._display.Context.Current()# 通过此方法可以获取尺寸
			dimension = AIS_LengthDimension.DownCast(dimension_shape)
			if dimension is not None or True:
				dimension_elements = self.Dimension_dict.keys()
				for element in dimension_elements:
					if dimension.GetTextPosition().IsEqual(self.Dimension_dict[element].GetTextPosition(), 0.001):
						self.parent.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(
							self.move_dimension)
						self.parent.parent.Displayshape_core.canva.mouseReleaseEvent_Signal.trigger.connect(
							self.move_dimension_end)
						self.selected_dimension_ID = element
			
		except Exception as e:
			print(e)
			pass
			pass
	def GB_Dimension(self,shape):
			pass
	# 创建尺寸
	def Delete_Dimension(self,shape):
		#删除尺寸
		pass
	def Update_Dimension(self,shape):
		#更新尺寸
		pass