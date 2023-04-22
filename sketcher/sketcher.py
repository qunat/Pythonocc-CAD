# -*- coding: utf-8 -*-
from OCC.Core.BRep import BRep_Tool
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire

from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.gp import gp_Pnt
from OCC.Core.AIS import AIS_Shape


class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.select_shape_list = []
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		
	def select_skecth_plane(self):
		self.select_windows=SelectWidget(parent=self.parent)
		self.select_windows.Show()
		
	def uptoplane(self):
		self.parent.InteractiveOperate.InteractiveModule="SKETCH"
		self.parent.Displayshape_core.canva._display.register_select_callback(self.clicked_callback)
		if self.select_windows.comboBox.currentText()=="XY平面":
			self.parent.Displayshape_core.canva._display.View_Top()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.do_draw()
		if self.select_windows.comboBox.currentText()=="YZ平面":
			self.parent.Displayshape_core.canva._display.View_Right()
			self.parent.Displayshape_core.canva._display.FitAll()
		if self.select_windows.comboBox.currentText()=="XZ平面":
			self.parent.Displayshape_core.canva._display.View_Front()
			self.parent.Displayshape_core.canva._display.FitAll()
	
	def clicked_callback(self, shp, *kwargs):
		try:
			
			self.new_do_draw.draw_line(shp)# draw line
		except Exception as e:
			print(e)
	def do_draw(self):
		self.new_do_draw=sketch_line(self.parent)# draw line
		
	def dynamics_drwa(self):
		self.new_do_draw.dynamics_drwa_line()# draw line
	
	
	
	
class sketch_line(object):
	def __init__(self, parent=None):
		self.parent = parent
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_line_dict = {}
		self.point_count = []
		self.line_id=0
		
	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					self.parent.Displayshape_core.canva.dragStartPosX,
					self.parent.Displayshape_core.canva.dragStartPosY)
				if shape!=None and  shape!=[] and not isinstance(shape,TopoDS_Wire) :
					P = BRep_Tool.Pnt(shape[0])
					x,y,z=P.X(),P.Y(),P.Z()
				
				if len(self.point_count) == 0:
					point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x, y, z), True,
																					  False)  # 重新计算更新已经显示的物
					self.point = (x, y, z)
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
					
				elif len(self.point_count) >= 1:
					self.InteractiveModule = None
					point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x, y, z), True,
																					  False)  # 重新计算更新已经显示的物
					aSegment = GC_MakeSegment(
						gp_Pnt(self.point_count[-1][0], self.point_count[-1][1], self.point_count[-1][2]),
						gp_Pnt(x, y, z))
					anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
					aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
					self.show_line_dict[self.line_id][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id][0], True,
																				   False)  # 重新计算更新已经显示的物体
					self.line_id+=1
					self.point_count.clear()
		
	def dynamics_drwa_line(self):
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					_dragStartPosX,
					_dragStartPosY)
				# print(x, y, z)
				try:
					x0 = self.point[0]
					y0 = self.point[1]
					z0 = self.point[2]
					aSegment = GC_MakeSegment(gp_Pnt(x0, y0, z0), gp_Pnt(x, y, z))
					anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
					aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
					
					if self.show_line_dict[self.line_id] == None:
						self.show_line_dict[self.line_id] = AIS_Shape(aWire)
						self.show_line_dict[self.line_id] = self.parent.Displayshape_core.canva._display.DisplayShape(aWire, True,
																								 False)  # 重新计算更新已经显示的物体
					else:
						self.show_line_dict[self.line_id][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id][0], True,
																				   False)  # 重新计算更新已经显示的物体
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				
				
				except Exception as e:
					pass
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY

			