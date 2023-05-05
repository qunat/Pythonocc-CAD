# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire, TopoDS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
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

class sketch_line(object):
	def __init__(self, parent=None,width=2,color=Quantity_NOC_BLACK):
		self.parent = parent
		self.width = width
		self.color=color
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_line_dict = {}
		self.point_count = []
		self.line_id=0
		#self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)

		


		
	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					self.parent.Displayshape_core.canva.dragStartPosX,
					self.parent.Displayshape_core.canva.dragStartPosY)
				
				if shape!=[] and isinstance(shape[0],TopoDS_Vertex) :#捕捉端点
					P = BRep_Tool.Pnt(shape[0])
					x,y,z=P.X(),P.Y(),P.Z()
					
				if shape!=[] and isinstance(shape[0],TopoDS_Wire) :#捕捉线上任意点
					direction = gp_Dir(vx, vy, vz)
					line = gp_Lin(gp_Pnt(x, y, z), direction)
					ais_line = Geom_Line(line)
					edge_builder = BRepBuilderAPI_MakeEdge(line)
					edge = edge_builder.Edge()
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(shape[0], edge)
					nearest_point = extrema.PointOnShape1(1)
					x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
					
				
				if len(self.point_count) == 0:
					self.draw_point(x,y,z)
					self.point = (x, y, z)
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)

					
					
				elif len(self.point_count) >= 1:
					self.InteractiveModule = None
					self.draw_point(x, y, z)# end point
					aSegment = GC_MakeSegment(
						gp_Pnt(self.point_count[-1][0], self.point_count[-1][1], self.point_count[-1][2]),
						gp_Pnt(x, y, z))
					anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
					aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
					self.show_line_dict[self.line_id].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
					self.show_line_dict[self.line_id].SetWidth(self.width)
					self.show_line_dict[self.line_id].SetColor(Quantity_Color(self.color))
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id], True,
																				   False)  # 重新计算更新已经显示的物体
					self.line_id+=1
					self.point_count.clear()

	def dynamics_draw_trance(self):
		Distance=0
		_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(_dragStartPosX,_dragStartPosY)
		direction = gp_Dir(vx, vy, vz)
		line = gp_Lin(gp_Pnt(x, y, z), direction)
		ais_line = Geom_Line(line)
		edge_builder = BRepBuilderAPI_MakeEdge(line)
		edge = edge_builder.Edge()
		for key in self.show_line_dict.keys():
			try:
				extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_line_dict[key].Shape(), edge)
				nearest_point1 = extrema.PointOnShape1(1)
				nearest_point2 = extrema.PointOnShape1(1)
				if Distance>nearest_point1.Distance(nearest_point2) or Distance==0:
					Distance=nearest_point1.Distance(nearest_point2)
					x, y, z = nearest_point1.X(), nearest_point1.Y(), nearest_point1.Z()
				pass
			except Exception as e:
				print(e)
				pass
		if len(self.show_line_dict.keys())!=0 and Distance<=1:
			ais_point=self.draw_point(x,y,z)

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
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id], True,)  # 重新计算更新已经显示的物体
					else:
						self.show_line_dict[self.line_id].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
						self.show_line_dict[self.line_id].SetWidth(self.width)
						self.show_line_dict[self.line_id].SetColor(Quantity_Color(self.color))
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id], True,
																				   False)  # 重新计算更新已经显示的物体
					self.parent.Displayshape_core.canva._display.Repaint()
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				
				
				except Exception as e:
					pass
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY
	

	def draw_point(self,x,y,z,point_type=None,color=None):
		ALL_ASPECTS = [Aspect_TOM_POINT,
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
					   Aspect_TOM_BALL]
		if point_type!=None:
			point_type = ALL_ASPECTS[point_type]
			p = Geom_CartesianPoint(gp_Pnt(x, y, z))
			color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
			ais_point = AIS_Point(p)
			
			drawer = ais_point.Attributes()
			asp = Prs3d_PointAspect(point_type, color, 4)
			drawer.SetPointAspect(asp)
			ais_point.SetAttributes(drawer)
			point = self.parent.Displayshape_core.canva._display.Context.Display(ais_point,
																				 False)  # 重新计算更新已经显示的物
		else:
			point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x,y,z),color="YELLOW",
																			update=False	 )  # 重新计算更新已经显示的物
			self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			self.parent.Displayshape_core.canva._display.Repaint()


		
			
