# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from GUI.SelectWidget import SelectWidget
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2,gp_Dir
from OCC.Core.AIS import AIS_Shape, AIS_Point
from OCC.Core.Aspect import (Aspect_TOM_POINT,
                             Aspect_TOM_PLUS,
                             Aspect_TOM_STAR,
                             Aspect_TOM_X,
                             Aspect_TOM_O,
                             Aspect_TOM_O_POINT,
                             Aspect_TOM_O_PLUS,
                             Aspect_TOM_O_STAR,
                             Aspect_TOM_O_X,
                             Aspect_TOM_RING1,
                             Aspect_TOM_RING2,
                             Aspect_TOM_RING3,
                             Aspect_TOM_BALL)

from sketcher.sketcher_line import sketch_line


class sketch_circel(sketch_line):
	def __init__(self,parent=None,gp_Dir=None):
		super(sketch_circel, self).__init__()
		self.parent = parent
		self.gp_Dir=gp_Dir
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_circel_dict = {}
		self.point_count = []
		self.circel_id = 0
	
	def draw_circel(self, shape=None):
		if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
				self.parent.Displayshape_core.canva.dragStartPosX,
				self.parent.Displayshape_core.canva.dragStartPosY)
			
			if shape != [] and isinstance(shape[0], TopoDS_Vertex):  # 捕捉端点
				P = BRep_Tool.Pnt(shape[0])
				x, y, z = P.X(), P.Y(), P.Z()
			
			if shape != [] and isinstance(shape[0], TopoDS_Wire):  # 捕捉线上任意点
				direction = gp_Dir(vx, vy, vz)
				line = gp_Lin(gp_Pnt(x, y, z), direction)
				ais_line = Geom_Line(line)
				edge_builder = BRepBuilderAPI_MakeEdge(line)
				edge = edge_builder.Edge()
				extrema = BRepExtrema.BRepExtrema_DistShapeShape(shape[0], edge)
				nearest_point = extrema.PointOnShape1(1)
				x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
			
			if len(self.point_count) == 0:
				self.draw_point(x, y, z)
				self.point = (x, y, z)
				self.point_count.append(self.point)
				self.show_circel_dict[self.circel_id] = None
				self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_circel)
			
			
			elif len(self.point_count) >= 1:
				self.InteractiveModule = None
				#self.draw_point(x, y, z)  # end point
				p1=gp_Pnt(self.point_count[-1][0], self.point_count[-1][1], self.point_count[-1][2])
				p2=gp_Pnt(x, y, z)
				radius=p1.Distance(p2)
				circel=GC_MakeCircle(p1,self.gp_Dir,radius).Value()
				circel_builder = BRepBuilderAPI_MakeEdge(circel)
				circel = circel_builder.Edge()
				self.show_circel_dict[self.circel_id][0].SetShape(circel)  # 将已经显示的零件设置成另外一个新零件
				self.show_circel_dict[self.circel_id][0].SetWidth(self.width)
				self.show_circel_dict[self.circel_id][0].SetColor(Quantity_Color(self.color))
				self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_circel_dict[self.circel_id][0],
																			   True,
																			   False)  # 重新计算更新已经显示的物体
				self.circel_id += 1
				self.point_count.clear()
	
	def dynamics_drwa_circel(self):
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
				p1 = gp_Pnt(x0,y0,z0)
				p2 = gp_Pnt(x, y, z)
				radius = p1.Distance(p2)
				circel = GC_MakeCircle(p1, self.gp_Dir, radius).Value()
				circel_builder = BRepBuilderAPI_MakeEdge(circel)
				circel = circel_builder.Edge()

				
				if self.show_circel_dict[self.circel_id] == None:
					self.show_circel_dict[self.circel_id] = AIS_Shape(circel)
					self.show_circel_dict[self.circel_id] = self.parent.Displayshape_core.canva._display.DisplayShape(circel,
																												  True,
																												  False)  # 重新计算更新已经显示的物体

				else:
					self.show_circel_dict[self.circel_id][0].SetShape(circel)  # 将已经显示的零件设置成另外一个新零件
					self.show_circel_dict[self.circel_id][0].SetWidth(self.width)
					self.show_circel_dict[self.circel_id][0].SetColor(Quantity_Color(self.color))
				self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_circel_dict[self.circel_id][0],
																			   True,
																			   False)  # 重新计算更新已经显示的物体
				self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			
			
			except Exception as e:
				#print(e)
				pass
		
		self.dragStartPosX = _dragStartPosX
		self.dragStartPosY = _dragStartPosY


